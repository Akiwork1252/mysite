from django.urls import path

from . import views


app_name = 'learning'
urlpatterns = [
    path('learning/<int:learning_topic>', views.LearningView.as_view(), name='learning'),
]
