from django.db import models
from apps.interviews.models import Interview


class Report(models.Model):
    STATUS_CHOICES = (
        ('generating', 'Generating'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )

    RECOMMENDATION_CHOICES = (
        ('strong_hire', 'Strong Hire'),
        ('hire', 'Hire'),
        ('maybe', 'Maybe'),
        ('no_hire', 'No Hire'),
        ('strong_no_hire', 'Strong No Hire'),
    )

    interview = models.OneToOneField(
        Interview,
        on_delete=models.CASCADE,
        related_name='report'
    )
    overall_score = models.FloatField()
    recommendation = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_CHOICES
    )
    summary = models.TextField()
    strengths = models.JSONField(default=list)
    improvements = models.JSONField(default=list)
    topic_scores = models.JSONField(default=dict)
    detailed_feedback = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='generating'
    )
    pdf_file = models.FileField(
        upload_to='reports/',
        blank=True,
        null=True
    )
    generated_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = 'reports'

    def __str__(self):
        return f"Report: {self.interview} - {self.recommendation}"

    @property
    def is_ready(self):
        return self.status == 'completed'