from django.db import models
from apps.interviews.models import InterviewQuestion


class AIEvaluation(models.Model):
    interview_question = models.OneToOneField(
        InterviewQuestion,
        on_delete=models.CASCADE,
        related_name='ai_evaluation'
    )
    score = models.FloatField()
    max_score = models.FloatField(default=10.0)
    feedback = models.TextField()
    strengths = models.JSONField(default=list)
    improvements = models.JSONField(default=list)
    keywords_matched = models.JSONField(default=list)
    keywords_missed = models.JSONField(default=list)
    confidence_level = models.CharField(
        max_length=20,
        default='medium'
    )
    evaluated_at = models.DateTimeField(
        auto_now_add=True
    )
    model_used = models.CharField(
        max_length=50,
        default='gpt-4'
    )
    tokens_used = models.PositiveIntegerField(
        default=0
    )

    class Meta:
        db_table = 'ai_evaluations'

    def __str__(self):
        return f"Score: {self.score}/{self.max_score}"

    @property
    def percentage_score(self):
        return (self.score / self.max_score) * 100

    @property
    def grade(self):
        percentage = self.percentage_score
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 50:
            return 'D'
        else:
            return 'F'