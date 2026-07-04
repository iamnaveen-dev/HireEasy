from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from apps.interviews.models import Interview, InterviewQuestion
from apps.interviews.serializers import (
    InterviewSerializer,
    CreateInterviewSerializer,
    UpdateInterviewStatusSerializer,
    InterviewQuestionSerializer,
)
from apps.questions.models import Question

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_interview_view(request):
    if not hasattr(request.user, 'company'):
        return Response({
            'error': 'Only company members can create interviews'
        }, status=status.HTTP_403_FORBIDDEN)
    serializer = CreateInterviewSerializer(
        data=request.data,
        context={'request': request}
    )
    if serializer.is_valid():
        interview = serializer.save()
        return Response({
            'message': 'Interview scheduled successfully',
            'interview': InterviewSerializer(interview).data,
            'room_code': interview.room_code,
            'join_link': f'/interview/join/{interview.room_code}',
        }, status=status.HTTP_201_CREATED)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_interviews_view(request):
    user = request.user
    if hasattr(user, 'company'):
        interviews = Interview.objects.filter(
            company=user.company
        ).select_related('candidate', 'interviewer')
    elif user.role == 'interviewer':
        interviews = Interview.objects.filter(
            interviewer=user
        ).select_related('candidate', 'interviewer')
    else:
        interviews = Interview.objects.filter(
            candidate=user
        ).select_related('candidate', 'interviewer')
    serializer = InterviewSerializer(interviews, many=True)
    return Response({
        'total': interviews.count(),
        'interviews': serializer.data,
    })
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_interview_view(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except Interview.DoesNotExist:
        return Response({
            'error': 'Interview not found'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = InterviewSerializer(interview)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def join_interview_view(request, room_code):
    try:
        interview = Interview.objects.get(
            room_code=room_code
        )
    except Interview.DoesNotExist:
        return Response({
            'error': 'Invalid room code'
        }, status=status.HTTP_404_NOT_FOUND)
    user = request.user
    is_participant = (
        interview.candidate == user or
        interview.interviewer == user
    )
    if not is_participant:
        return Response({
            'error': 'You are not part of this interview'
        }, status=status.HTTP_403_FORBIDDEN)
    if interview.status == 'scheduled':
        interview.status = 'waiting'
        interview.save()
    return Response({
        'message': f'Joined interview room {room_code}',
        'interview': InterviewSerializer(interview).data,
        'your_role': 'candidate' if interview.candidate == user else 'interviewer',
    })
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_interview_status_view(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except Interview.DoesNotExist:
        return Response({
            'error': 'Interview not found'
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = UpdateInterviewStatusSerializer(
        data=request.data
    )
    if serializer.is_valid():
        new_status = serializer.validated_data['status']
        notes = serializer.validated_data.get(
            'interviewer_notes', ''
        )
        if new_status == 'in_progress':
            interview.started_at = timezone.now()
        elif new_status == 'completed':
            interview.ended_at = timezone.now()
        interview.status = new_status
        if notes:
            interview.interviewer_notes = notes
        interview.save()
        return Response({
            'message': f'Interview status updated to {new_status}',
            'interview': InterviewSerializer(interview).data,
        })
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_question_to_interview_view(request, pk):
    try:
        interview = Interview.objects.get(pk=pk)
    except Interview.DoesNotExist:
        return Response({
            'error': 'Interview not found'
        }, status=status.HTTP_404_NOT_FOUND)
    question_id = request.data.get('question_id')
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        return Response({
            'error': 'Question not found'
        }, status=status.HTTP_404_NOT_FOUND)
    order = interview.interview_questions.count() + 1
    interview_question = InterviewQuestion.objects.create(
        interview=interview,
        question=question,
        order=order
    )
    question.times_asked += 1
    question.save()
    return Response({
        'message': 'Question added to interview',
        'interview_question': InterviewQuestionSerializer(
            interview_question
        ).data,
    }, status=status.HTTP_201_CREATED)
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def submit_answer_view(request, pk, iq_pk):
    try:
        interview_question = InterviewQuestion.objects.get(
            pk=iq_pk,
            interview__id=pk
        )
    except InterviewQuestion.DoesNotExist:
        return Response({
            'error': 'Question not found in this interview'
        }, status=status.HTTP_404_NOT_FOUND)
    answer = request.data.get('candidate_answer', '')
    time_taken = request.data.get('time_taken_seconds', 0)
    interview_question.candidate_answer = answer
    interview_question.time_taken_seconds = time_taken
    interview_question.save()
    return Response({
        'message': 'Answer submitted successfully',
        'interview_question': InterviewQuestionSerializer(
            interview_question
        ).data,
    })



        

        

        
    







        


    
    

    
