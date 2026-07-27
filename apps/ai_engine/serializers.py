from rest_framework import serializers
from apps.ai_engine.models import AIEvaluation

class AIEvaluationSerializer(serializers.ModelSerializer):
    grade=serializers.CharField(
        source='grade', 
        read_only=True
        )
    percentage_score=serializers.FloatField(
        source='percentage_score',
        read_only=True
        )
    class Meta:
        model=  AIEvaluation
        fields=[
            'id',
            'score',
            'max_score',
            'feedback',
            'strengths',
            'improvements',
            'keywords_matched',
            'keywords_missed',
            'confidence_level',
            'grade',
            'percentage_score',
            'evaluated_at',
            'model_used',
            'tokens_used'

        ]
        read_only_fields=[
             'id',
            'grade',
            'percentage_score',
            'evaluated_at',
            'model_used',
            'tokens_used',
        ]