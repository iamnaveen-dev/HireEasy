from django.urls import path
from apps.questions import views

urlpatterns = [
    path(
        'create/',
        views.create_question_view,
        name='create_question'
    ),
    path(
        '',
        views.list_questions_view,
        name='list_questions'
    ),
    path(
        'mine/',
        views.my_questions_view,
        name='my_questions'
    ),
    path(
        '<int:pk>/',
        views.get_question_view,
        name='get_question'
    ),
    path(
        '<int:pk>/update/',
        views.update_question_view,
        name='update_question'
    ),
    path(
        '<int:pk>/delete/',
        views.delete_question_view,
        name='delete_question'
    ),
]