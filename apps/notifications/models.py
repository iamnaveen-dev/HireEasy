from django.db import models
from apps.users.models import User


class Notification(models.Model):

    TYPE_CHOICES = (
        ('interview_scheduled', 'Interview Scheduled'),
        ('interview_started', 'Interview Started'),
        ('interview_completed', 'Interview Completed'),
        ('report_ready', 'Report Ready'),
        ('score_updated', 'Score Updated'),
        ('invitation', 'Invitation'),
        ('reminder', 'Reminder'),
    )

    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(
        max_length=30,
        choices=TYPE_CHOICES
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(
        default=dict,
        blank=True
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username} - {self.title}"