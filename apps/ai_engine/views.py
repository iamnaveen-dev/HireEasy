from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.ai_engine.models import AIEvaluation
from apps.ai_engine.serializers import AIEvaluationSerializer
from apps.ai_engine.evaluator import evaluate_answer
from apps.interviews.models import InterviewQuestion


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def evaluate_answer_view(request, iq_pk):
    try:
        interview_question = InterviewQuestion.objects.get(
            pk=iq_pk
        )
    except InterviewQuestion.DoesNotExist:
        return Response({
            'error': 'Interview question not found'
        }, status=status.HTTP_404_NOT_FOUND)

    if not interview_question.candidate_answer:
        return Response({
            'error': 'No answer submitted yet'
        }, status=status.HTTP_400_BAD_REQUEST)

    question = interview_question.question
    evaluation_data = evaluate_answer(
        question_title=question.title,
        question_description=question.description,
        expected_answer=question.expected_answer,
        candidate_answer=interview_question.candidate_answer,
        difficulty=question.difficulty
    )

    evaluation, created = AIEvaluation.objects.update_or_create(
        interview_question=interview_question,
        defaults={
            'score': evaluation_data['score'],
            'feedback': evaluation_data['feedback'],
            'strengths': evaluation_data.get('strengths', []),
            'improvements': evaluation_data.get('improvements', []),
            'keywords_matched': evaluation_data.get('keywords_matched', []),
            'keywords_missed': evaluation_data.get('keywords_missed', []),
            'confidence_level': evaluation_data.get('confidence_level', 'medium'),
            'tokens_used': evaluation_data.get('tokens_used', 0),
            'model_used': evaluation_data.get('model_used', 'gpt-4'),
        }
    )

    interview_question.ai_score = evaluation_data['score']
    interview_question.ai_feedback = evaluation_data['feedback']
    interview_question.save()

    return Response({
        'message': 'Answer evaluated successfully',
        'evaluation': AIEvaluationSerializer(evaluation).data,
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_evaluation_view(request, iq_pk):
    try:
        interview_question = InterviewQuestion.objects.get(
            pk=iq_pk
        )
        evaluation = interview_question.ai_evaluation
    except InterviewQuestion.DoesNotExist:
        return Response({
            'error': 'Interview question not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except AIEvaluation.DoesNotExist:
        return Response({
            'error': 'No evaluation found for this answer'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = AIEvaluationSerializer(evaluation)
    return Response(serializer.data)