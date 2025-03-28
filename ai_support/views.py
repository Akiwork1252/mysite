from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic, View

from .ai_survices import ai_generate_learning_task
from task_manager.models import LearningMainTopic, LearningSubTopic


# テスト生成
def generate_choice_test():
    pass
