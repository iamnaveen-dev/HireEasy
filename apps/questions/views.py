from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q
from apps.questions.models import Question
from apps.questions.serializers import (
    QuestionSerializer,
    CreateQuestionSerializer,
    UpdateQuestionSerializer,
)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question_view(request):
    serializer = CreateQuestionSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        question = serializer.save()
        return Response({
            'message': 'Question created successfully',
            'question': QuestionSerializer(question).data,
        }, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_questions_view(request):
    questions = Question.objects.filter(
        is_active=True
    ).select_related('created_by')

    topic = request.query_params.get('topic')
    difficulty = request.query_params.get('difficulty')
    question_type = request.query_params.get('type')
    search = request.query_params.get('search')

    if topic:
        questions = questions.filter(topic=topic)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)
    if question_type:
        questions = questions.filter(question_type=question_type)
    if search:
        questions = questions.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search)
        )

    serializer = QuestionSerializer(questions, many=True)
    return Response({
        'total': questions.count(),
        'questions': serializer.data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_question_view(request, pk):
    try:
        question = Question.objects.get(pk=pk)
    except Question.DoesNotExist:
        return Response({
            'error': 'Question not found'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = QuestionSerializer(question)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_question_view(request, pk):
    try:
        question = Question.objects.get(
            pk=pk,
            created_by=request.user
        )
    except Question.DoesNotExist:
        return Response({
            'error': 'Question not found or you do not have permission'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = UpdateQuestionSerializer(
        question,
        data=request.data,
        partial=request.method == 'PATCH'
    )
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Question updated successfully',
            'question': QuestionSerializer(question).data,
        })
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_question_view(request, pk):
    try:
        question = Question.objects.get(
            pk=pk,
            created_by=request.user
        )
    except Question.DoesNotExist:
        return Response({
            'error': 'Question not found or you do not have permission'
        }, status=status.HTTP_404_NOT_FOUND)
    question.is_active = False
    question.save()
    return Response({
        'message': 'Question deleted successfully'
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_questions_view(request):
    questions = Question.objects.filter(
        created_by=request.user,
        is_active=True
    ).select_related('created_by')
    serializer = QuestionSerializer(questions, many=True)
    return Response({
        'total': questions.count(),
        'questions': serializer.data,
    })