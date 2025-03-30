from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic, View

from task_manager.models import LearningSubTopic


# Create your views here.
class LearningView(LoginRequiredMixin, View):
    template_name = 'learning/learning.html'

    def get(self, request, *args, **kwargs):
        learning_topic_id = self.kwargs['learning_topic']
        learning_topic = get_object_or_404(LearningSubTopic, id=learning_topic_id)

        context = {'learning_topic': learning_topic}
        return render(request, 'learning/learning.html', context)
