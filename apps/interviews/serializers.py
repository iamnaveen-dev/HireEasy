from rest_framework import serializers
from apps.interviews.models import Interview, InterviewQuestion
from apps.users.models import User
from apps.users.serializers import UserSerializer
from apps.questions.serializers import QuestionSerializer


class InterviewSerializer(serializers.ModelSerializer):

    candidate = UserSerializer(read_only=True)
    interviewer = UserSerializer(read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    interview_type_display = serializers.CharField(
        source='get_interview_type_display',
        read_only=True
    )

    class Meta:
        model = Interview
        fields = [
            'id',
            'room_code',
            'candidate',
            'interviewer',
            'interview_type',
            'interview_type_display',
            'topics',
            'difficulty_level',
            'status',
            'status_display',
            'scheduled_at',
            'started_at',
            'ended_at',
            'duration_minutes',
            'overall_score',
            'interviewer_notes',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'room_code',
            'candidate',
            'interviewer',
            'overall_score',
            'started_at',
            'ended_at',
            'created_at',
        ]


class CreateInterviewSerializer(serializers.Serializer):

    candidate_email = serializers.EmailField(required=True)
    interview_type = serializers.ChoiceField(
        choices=[
            ('technical', 'Technical'),
            ('behavioural', 'Behavioural'),
            ('system_design', 'System Design'),
            ('coding', 'Coding Round'),
            ('hr', 'HR Round'),
            ('mixed', 'Mixed'),
        ],
        default='technical'
    )
    topics = serializers.ListField(
        child=serializers.CharField(),
        required=True
    )
    difficulty_level = serializers.ChoiceField(
        choices=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard'),
        ],
        default='medium'
    )
    scheduled_at = serializers.DateTimeField(required=True)
    duration_minutes = serializers.IntegerField(
        default=60,
        min_value=15,
        max_value=180
    )

    def validate_candidate_email(self, value):
        users = User.objects.filter(email=value)
        if not users.exists():
            raise serializers.ValidationError(
                'No candidate found with this email'
            )
        return value

    def create(self, validated_data):
        request = self.context.get('request')
        candidate_email = validated_data.pop('candidate_email')

        candidate = User.objects.filter(
            email=candidate_email
        ).first()

        if not candidate:
            raise serializers.ValidationError(
                'Candidate not found'
            )

        try:
            company = request.user.company
        except Exception:
            raise serializers.ValidationError(
                'You do not have a company registered'
            )

        interview = Interview.objects.create(
            interviewer=request.user,
            candidate=candidate,
            company=company,
            **validated_data
        )
        return interview


class UpdateInterviewStatusSerializer(serializers.Serializer):

    status = serializers.ChoiceField(
        choices=[
            ('waiting', 'Waiting'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ]
    )
    interviewer_notes = serializers.CharField(
        required=False,
        allow_blank=True
    )


class InterviewQuestionSerializer(serializers.ModelSerializer):

    question = QuestionSerializer(read_only=True)

    class Meta:
        model = InterviewQuestion
        fields = [
            'id',
            'question',
            'order',
            'candidate_answer',
            'ai_score',
            'ai_feedback',
            'time_taken_seconds',
            'is_skipped',
            'asked_at',
        ]
        read_only_fields = [
            'id',
            'question',
            'ai_score',
            'ai_feedback',
            'asked_at',
        ]