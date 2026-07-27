from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from apps.interviews.models import Interview, InterviewQuestion
from apps.reports.models import Report
import json


def calculate_overall_score(interview):
    questions = InterviewQuestion.objects.filter(
        interview=interview,
        candidate_answer__isnull=False
    ).exclude(candidate_answer='')

    if not questions.exists():
        return 0.0, {}

    total_score = 0.0
    count = 0
    topic_scores = {}
    topic_counts = {}

    for iq in questions:
        if iq.ai_score is not None:
            score = float(iq.ai_score)
            total_score += score
            count += 1
            topic = iq.question.topic
            if topic not in topic_scores:
                topic_scores[topic] = 0.0
                topic_counts[topic] = 0
            topic_scores[topic] += score
            topic_counts[topic] += 1

    if count == 0:
        return 0.0, {}

    overall = round(total_score / count, 2)
    topic_averages = {}
    for topic in topic_scores:
        topic_averages[topic] = round(
            topic_scores[topic] / topic_counts[topic], 2
        )

    return overall, topic_averages


def get_recommendation(score):
    if score >= 8.5:
        return 'strong_hire'
    elif score >= 7.0:
        return 'hire'
    elif score >= 5.5:
        return 'maybe'
    elif score >= 3.0:
        return 'no_hire'
    else:
        return 'strong_no_hire'


def generate_report_content(interview, overall_score, topic_scores):
    questions = InterviewQuestion.objects.filter(
        interview=interview
    ).select_related('question')

    strengths = []
    improvements = []

    for iq in questions:
        if iq.ai_score is not None:
            if float(iq.ai_score) >= 7.0:
                strengths.append(
                    f"Strong in {iq.question.topic}: {iq.question.title}"
                )
            else:
                improvements.append(
                    f"Needs improvement in {iq.question.topic}: {iq.question.title}"
                )

    recommendation = get_recommendation(overall_score)

    summary = f"""
Interview Performance Summary for {interview.candidate.username}

Overall Score: {overall_score}/10
Recommendation: {recommendation.replace('_', ' ').title()}

The candidate demonstrated knowledge across {len(topic_scores)} topics.
Topics covered: {', '.join(topic_scores.keys())}

{'Strong performance overall.' if overall_score >= 7.0 else 'Performance needs improvement in several areas.'}
    """.strip()

    return {
        'summary': summary,
        'strengths': strengths[:5],
        'improvements': improvements[:5],
        'recommendation': recommendation,
        'detailed_feedback': f"Candidate scored {overall_score}/10 overall across all questions."
    }


@shared_task
def generate_report_task(interview_id):
    try:
        interview = Interview.objects.get(id=interview_id)
    except Interview.DoesNotExist:
        return {'error': 'Interview not found'}

    report, created = Report.objects.get_or_create(
        interview=interview,
        defaults={'status': 'generating', 'overall_score': 0.0,
                  'recommendation': 'maybe', 'summary': 'Generating...',
                  'detailed_feedback': ''}
    )

    try:
        overall_score, topic_scores = calculate_overall_score(interview)
        report_content = generate_report_content(
            interview, overall_score, topic_scores
        )

        report.overall_score = overall_score
        report.recommendation = report_content['recommendation']
        report.summary = report_content['summary']
        report.strengths = report_content['strengths']
        report.improvements = report_content['improvements']
        report.topic_scores = topic_scores
        report.detailed_feedback = report_content['detailed_feedback']
        report.status = 'completed'
        report.save()

        interview.overall_score = overall_score
        interview.save()

        try:
            send_mail(
                subject=f'Interview Report: {interview.candidate.username}',
                message=f"""
Dear {interview.interviewer.username},

The interview report for {interview.candidate.username} is ready.

Overall Score: {overall_score}/10
Recommendation: {report_content['recommendation'].replace('_', ' ').title()}

Login to HireLinq to view the full report.

Best regards,
HireLinq Team
                """,
                from_email=settings.EMAIL_HOST_USER or 'noreply@hirelinq.com',
                recipient_list=[interview.interviewer.email],
                fail_silently=True,
            )
        except Exception:
            pass

        return {
            'status': 'success',
            'report_id': str(report.id),
            'overall_score': overall_score,
            'recommendation': report_content['recommendation']
        }

    except Exception as e:
        report.status = 'failed'
        report.save()
        return {'error': str(e)}