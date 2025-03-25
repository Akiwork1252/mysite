import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

from .forms import InquiryForm, AddInterestCategoryForm
from .models import UserInterestCategory


logger = logging.getLogger(__name__)

# トップ画面
class IndexView(generic.TemplateView):
    template_name = 'task_manager/index.html'


# お問い合わせ画面
class InquiryView(generic.FormView):
    form_class = InquiryForm
    template_name = 'task_manager/inquiry.html'
    success_url = reverse_lazy('task_manager:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        name = form.cleaned_data['name']
        logger.info(f'Inquiry sent by {name}')
        return super().form_valid(form)


# 興味カテゴリリスト画面
class InterestCategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/interest_category_list.html'
    context_object_name = 'interest_categories'

    def get_queryset(self):
        return self.request.user.interest_categories.all()


# 興味カテゴリ追加画面
class AddInterestCategoryView(LoginRequiredMixin, generic.FormView):
    form_class = AddInterestCategoryForm
    template_name = 'task_manager/add_interest_category.html'
    success_url = reverse_lazy('task_manager:interest_category')

    def form_valid(self, form):
        user_interest = form.save(commit=False)
        user_interest.user = self.request.user
        user_interest.save()
        return super().form_valid(form)


# 興味カテゴリ(関連付け)削除画面
class DeleteInterestCategory(LoginRequiredMixin, generic.DeleteView):
    model = UserInterestCategory
    template_name = 'task_manager/confirm_delete.html'
    success_url = reverse_lazy('task_manager:interest_category')

    def get_object(self, queryset = ...):
        category_id = self.kwargs['category_id']
        return get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            category__id=category_id,
        )
