from django.db import models
from apps.users.models import User
from apps.companies.models import Company
from apps.questions.models import Question
import uuid


class Interview(models.Model):
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('waiting', 'Waiting'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )

    INTERVIEW_TYPE_CHOICES = (
        ('technical', 'Technical'),
        ('behavioural', 'Behavioural'),
        ('system_design', 'System Design'),
        ('coding', 'Coding Round'),
        ('hr', 'HR Round'),
        ('mixed', 'Mixed'),
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    room_code = models.CharField(
        max_length=10,
        unique=True,
        blank=True
    )
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='candidate_interviews'
    )
    interviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interviewer_interviews'
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='interviews'
    )
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
        default='technical'
    )
    topics = models.JSONField(default=list)
    difficulty_level = models.CharField(
        max_length=10,
        default='medium'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    scheduled_at = models.DateTimeField()
    started_at = models.DateTimeField(
        blank=True,
        null=True
    )
    ended_at = models.DateTimeField(
        blank=True,
        null=True
    )
    duration_minutes = models.PositiveIntegerField(
        default=60
    )
    overall_score = models.FloatField(
        default=0.0
    )
    interviewer_notes = models.TextField(
        blank=True,
        null=True
    )
    is_recorded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'interviews'
        ordering = ['-scheduled_at']

    def save(self, *args, **kwargs):
        if not self.room_code:
            self.room_code = self._generate_room_code()
        super().save(*args, **kwargs)

    def _generate_room_code(self):
        import random
        import string
        return ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=8
            )
        )

    def __str__(self):
        return f"{self.candidate.username} | {self.interviewer.username} | {self.status}"


class InterviewQuestion(models.Model):
    interview = models.ForeignKey(
        Interview,
        on_delete=models.CASCADE,
        related_name='interview_questions'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='interview_appearances'
    )
    order = models.PositiveIntegerField(default=1)
    candidate_answer = models.TextField(
        blank=True,
        null=True
    )
    ai_score = models.FloatField(
        blank=True,
        null=True
    )
    ai_feedback = models.TextField(
        blank=True,
        null=True
    )
    time_taken_seconds = models.PositiveIntegerField(
        default=0
    )
    is_skipped = models.BooleanField(default=False)
    asked_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'interview_questions'
        ordering = ['order']

    def __str__(self):
        return f"Q{self.order}: {self.question.title[:50]}"