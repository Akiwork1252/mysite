from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import generic, View

from ai_support.ai_survices import lectures_by_ai
from task_manager.models import LearningSubTopic


# Create your views here.
class LearningView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        learning_topic_id = self.kwargs['learning_topic']
        learning_topic = get_object_or_404(LearningSubTopic, id=learning_topic_id)

        ai_lecture = lectures_by_ai(learning_topic.sub_topic)

        context = {
            'learning_topic': learning_topic,
            'ai_lecture': ai_lecture
            }
        
        return render(request, 'learning/learning.html', context)

