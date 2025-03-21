import logging

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm


logger = logging.getLogger(__name__)

# トップ画面
class IndexView(generic.TemplateView):
    template_name = 'task_manager/index.html'


# お問い合わせ画面
class InquiryView(generic.FormView):
    template_name = 'task_manager/inquiry.html'
    form_class = InquiryForm
    success_url = reverse_lazy('task_manager:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        name = form.cleaned_data['name']
        logger.info(f'Inquiry sent by {name}')
        return super().form_valid(form)
