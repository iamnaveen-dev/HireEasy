from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import FileResponse
from apps.reports.models import Report
from apps.reports.serializers import ReportSerializer, ReportListSerializer
from apps.reports.tasks import generate_report_task
from apps.interviews.models import Interview
import os


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_reports_view(request):
    user = request.user
    if hasattr(user, 'company'):
        reports = Report.objects.filter(
            interview__company=user.company
        ).select_related(
            'interview__candidate',
            'interview__interviewer'
        ).order_by('-generated_at')
    else:
        reports = Report.objects.filter(
            interview__candidate=user
        ).select_related(
            'interview__candidate',
            'interview__interviewer'
        ).order_by('-generated_at')

    serializer = ReportListSerializer(reports, many=True)
    return Response({
        'total': reports.count(),
        'reports': serializer.data,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_report_view(request, pk):
    try:
        report = Report.objects.get(pk=pk)
    except Report.DoesNotExist:
        return Response({
            'error': 'Report not found'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ReportSerializer(report)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_interview_report_view(request, interview_pk):
    try:
        interview = Interview.objects.get(pk=interview_pk)
        report = interview.report
    except Interview.DoesNotExist:
        return Response({
            'error': 'Interview not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Report.DoesNotExist:
        return Response({
            'error': 'Report not generated yet',
            'message': 'Report is being generated. Please check back in a moment.'
        }, status=status.HTTP_404_NOT_FOUND)

    serializer = ReportSerializer(report)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def regenerate_report_view(request, interview_pk):
    try:
        interview = Interview.objects.get(pk=interview_pk)
    except Interview.DoesNotExist:
        return Response({
            'error': 'Interview not found'
        }, status=status.HTTP_404_NOT_FOUND)

    generate_report_task.delay(str(interview.id))

    return Response({
        'message': 'Report generation started',
        'interview_id': str(interview.id),
    })