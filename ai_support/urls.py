from django.urls import path

from . import views


urlpatterns = [
    path('ai_support/create_learning_task/', views.CreateLearningTask.as_view(), name='create_learning_task'),
]
