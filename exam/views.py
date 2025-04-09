from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.shortcuts import render


# Create your views here.
class MultipleChoiceQuestionsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'exam/multiple_choice_questions.html'