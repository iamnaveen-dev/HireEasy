from django.urls import path
from apps.reports import views

urlpatterns = [
    path(
        '',
        views.list_reports_view,
        name='list_reports'
    ),
    path(
        '<int:pk>/',
        views.get_report_view,
        name='get_report'
    ),
    path(
        'interview/<str:interview_pk>/',
        views.get_interview_report_view,
        name='get_interview_report'
    ),
    path(
        'interview/<str:interview_pk>/regenerate/',
        views.regenerate_report_view,
        name='regenerate_report'
    ),
]