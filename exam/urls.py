from django.urls import path

from . import views


app_name = 'exam'
urlpatterns = [
    # 選択問題
    path('multiple_choice_questions/main/<int:topic_id>', views.MultipleChoiceQuestionsView.as_view(), name='multiple_choice_questions_main'),
    path('multiple_choice_questions/sub/<int:topic_id>', views.MultipleChoiceQuestionsView.as_view(), name='multiple_choice_questions_sub'),
    # 記述問題
    path('constructed_question/main/<int:topic_id>', views.ConstructedQuestionView.as_view(), name='constructed_question_main'),
    path('constructed_question/sub/<int:topic_id>', views.ConstructedQuestionView.as_view(), name='constructed_question_sub'),
    # 総合問題
    path('integrated_question/<int:learning_objective_id>', views.IntegratedQuestionView.as_view(), name='integrated_question'),
]
