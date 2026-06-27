from rest_framework import serializers
from apps.questions.models import Question
from apps.users.serializers import UserSerializer

class QuestionSerializer(serializers.ModelSerializer):
    created_by=UserSerializer(read_only=True)
    difficulty_display=serializers.CharField(
        source='get_difficulty_display', 
        read_only=True
    )
    topic_display=serializers.CharField(
        source='get_topic_display', 
        read_only=True
    )
    question_type_display=serializers.CharField(
        source='get_question_type_display', 
        read_only=True
    )
    class Meta:
        model=Question
        fields=[
            'id',
            'title',
            'description',
            'topic',
            'topic_display',
            'difficulty',
            'difficulty_display',
            'question_type',
            'question_type_display',
            'expected_answer',
            'follow_up_questions',
            'tags',
            'created_by',
            'is_active',
            'times_asked',
            'average_score',
            'created_at',
            'updated_at',

        ]
        read_only_fields=[
            'id',
            'created_by',
            'times_asked',
            'average_score',
            'created_at',
            'updated_at',

        ]
class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Question
        fields=[
            'title',
            'description',
            'topic',
            'difficulty',
            'question_type',
            'expected_answer',
            'follow_up_questions',
            'tags',


        ]
    def create(self, validated_data):
        request = self.context.get('request')
        question = Question.objects.create(
            created_by=request.user,
            **validated_data
        )
        return question
class UpdateQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Question
        fields = [
            'title',
            'description',
            'topic',
            'difficulty',
            'question_type',
            'expected_answer',
            'follow_up_questions',
            'tags',
            'is_active',
        ]


       

