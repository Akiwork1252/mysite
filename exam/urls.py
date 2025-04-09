from django.urls import path

from . import views


app_name = 'exam'
urlpatterns = [
    path('multiple_choice_questions/<int:topic_id>', views.MultipleChoiceQuestionsView.as_view(), name='multiple_choice_questions'),
]
