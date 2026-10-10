from rest_framework import serializers
from apps.reports.models import Report
from apps.interviews.serializers import InterviewSerializer


class ReportSerializer(serializers.ModelSerializer):

    interview = InterviewSerializer(read_only=True)
    recommendation_display = serializers.CharField(
        source='get_recommendation_display',
        read_only=True
    )
    is_ready = serializers.BooleanField(
        
        read_only=True
    )

    class Meta:
        model = Report
        fields = [
            'id',
            'interview',
            'overall_score',
            'recommendation',
            'recommendation_display',
            'summary',
            'strengths',
            'improvements',
            'topic_scores',
            'detailed_feedback',
            'status',
            'is_ready',
            'pdf_file',
            'generated_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'overall_score',
            'recommendation',
            'summary',
            'strengths',
            'improvements',
            'topic_scores',
            'detailed_feedback',
            'status',
            'generated_at',
            'updated_at',
        ]


class ReportListSerializer(serializers.ModelSerializer):

    candidate_name = serializers.CharField(
        source='interview.candidate.username',
        read_only=True
    )
    interviewer_name = serializers.CharField(
        source='interview.interviewer.username',
        read_only=True
    )
    recommendation_display = serializers.CharField(
        source='get_recommendation_display',
        read_only=True
    )

    class Meta:
        model = Report
        fields = [
            'id',
            'candidate_name',
            'interviewer_name',
            'overall_score',
            'recommendation',
            'recommendation_display',
            'status',
            'generated_at',
        ]

        