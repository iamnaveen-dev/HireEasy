from django.urls import path
from apps.ai_engine import views

urlpatterns = [
    path(
        'evaluate/<int:iq_pk>/',
        views.evaluate_answer_view,
        name='evaluate_answer'
    ),
    path(
        'evaluation/<int:iq_pk>/',
        views.get_evaluation_view,
        name='get_evaluation'
    ),
]