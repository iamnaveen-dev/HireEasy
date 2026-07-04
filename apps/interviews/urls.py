from django.urls import path
from apps.interviews import views

urlpatterns = [
    path(
        'create/',
        views.create_interview_view,
        name='create_interview'
    ),
    path(
        '',
        views.list_interviews_view,
        name='list_interviews'
    ),
    path(
        'join/<str:room_code>/',
        views.join_interview_view,
        name='join_interview'
    ),
    path(
        '<str:pk>/',
        views.get_interview_view,
        name='get_interview'
    ),
    path(
        '<str:pk>/status/',
        views.update_interview_status_view,
        name='update_interview_status'
    ),
    path(
        '<str:pk>/questions/add/',
        views.add_question_to_interview_view,
        name='add_question'
    ),
    path(
        '<str:pk>/questions/<int:iq_pk>/answer/',
        views.submit_answer_view,
        name='submit_answer'
    ),
]