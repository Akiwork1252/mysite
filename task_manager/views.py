import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic, View

from .forms import InquiryForm, AddInterestCategoryForm, SettingLearningObjectiveForm
from .models import Category, UserInterestCategory, LearningObjective, LearningMainTopic, LearningSubTopic
from ai_support.ai_survices import ai_generate_learning_task


logger = logging.getLogger(__name__)

# トップ画面
class IndexView(generic.TemplateView):
    template_name = 'task_manager/index.html'


# お問い合わせフォーム
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

# ========== 興味カテゴリ ==========
# リスト表示
class InterestCategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = 'task_manager/interest_category_list.html'
    context_object_name = 'interest_categories'

    def get_queryset(self):
        return self.request.user.interest_categories.all()


# 追加
class AddInterestCategoryView(LoginRequiredMixin, generic.FormView):
    form_class = AddInterestCategoryForm
    template_name = 'task_manager/add_interest_category.html'
    success_url = reverse_lazy('task_manager:interest_category')

    def form_valid(self, form):
        user_interest = form.save(commit=False)
        user_interest.user = self.request.user
        user_interest.save()
        return super().form_valid(form)


# 削除
class DeleteInterestCategory(LoginRequiredMixin, generic.DeleteView):
    model = UserInterestCategory
    template_name = 'task_manager/confirm_delete_category.html'
    success_url = reverse_lazy('task_manager:interest_category')

    def get_object(self, queryset = ...):
        category_id = self.kwargs['category_id']
        return get_object_or_404(
            UserInterestCategory,
            user=self.request.user,
            category__id=category_id,
        )


# ========== 学習目標 ==========
# リスト表示
class LearningObjectiveListView(LoginRequiredMixin, generic.ListView):
    model = LearningObjective
    context_object_name = 'learning_objectives'
    template_name = 'task_manager/learning_objective_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        context['category'] = get_object_or_404(Category, id=category_id)
        return context
    
    def get_queryset(self):
        category = self.kwargs['category_id']
        return LearningObjective.objects.filter(
            user=self.request.user,
            category_id=category,
        )


# 目標設定 + タスク生成
class SettingLearningObjectiveView(LoginRequiredMixin, generic.FormView):
    form_class = SettingLearningObjectiveForm
    template_name = 'task_manager/setting_learning_objective.html'
    success_url = reverse_lazy('task_manager:preview_generated_task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id = self.kwargs['category_id']
        category = get_object_or_404(Category, id=category_id)
        context["category"] = category
        # セッションに保存(プレビュー後の画面推移に使用)
        self.request.session['category_id'] = category.id

        return context
        
    def form_valid(self, form):
        title = form.cleaned_data['title']
        current_level = form.cleaned_data['current_level']
        target_level = form.cleaned_data['target_level']
        # 学習タスクを生成
        generated_tasks = ai_generate_learning_task(title, current_level, target_level)
        # セッションに保存
        self.request.session['generated_tasks'] = generated_tasks
        self.request.session['title'] = title
        self.request.session['current_level'] = current_level
        self.request.session['target_level'] = target_level

        return super().form_valid(form)


# 生成タスクの確認、決定
class PreviewGeneratedTask(LoginRequiredMixin, generic.TemplateView):
    template_name = 'task_manager/preview_of_the_generated_task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        category_id = self.request.session.get('category_id')

        context['category_id'] = category_id
        context["title"] = self.request.session.get('title')
        context['generated_tasks'] = self.request.session.get('generated_tasks')

        return context


# 学習目標・学習タスクの保存
class SaveLearningTask(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):

        # ユーザーが入力した学習目標の設定をセッションから取得
        title = request.session.get('title')
        current_level = request.session.get('current_level')
        target_level = request.session.get('target_level')
        
        # 学習目標が属するカテゴリを取得
        category_id = request.session.get('category_id')
        category = get_object_or_404(Category, id=category_id)

        # 学習目標保存
        learning_objective = LearningObjective.objects.create(
            user=request.user,
            category=category,
            title=title,
            current_level=current_level,
            target_level=target_level,
        )

        # リダイレクト用に学習目標idを取得
        learning_objective_id = learning_objective.id

        # トピック名とそのオブジェクトでメイントピックの辞書を作成
        main_topic_objs = {}

        # 学習タスク保存(main_topic)
        selected_main_topics = request.POST.getlist('main_topics')
        for main_topic_name in selected_main_topics:
            main_topic_obj = LearningMainTopic.objects.create(
                user=request.user,
                learning_objective=learning_objective,
                main_topic=main_topic_name
            )
            main_topic_objs[main_topic_name] = main_topic_obj

        # 学習タスク保存(sub_topic)
        for main_topic_name, main_topic_obj in main_topic_objs.items():
            # main_topicごとのname属性で取得
            selected_sub_topics = request.POST.getlist(f'sub_topics_{main_topic_name}')
            for sub_topic_name in selected_sub_topics:
                LearningSubTopic.objects.create(
                    main_topic=main_topic_obj,
                    sub_topic=sub_topic_name,
                )

        return redirect('task_manager:learning_task_list', learning_objective_id=learning_objective_id )


# 学習目標削除
class DeleteLerningObjectiveView(LoginRequiredMixin, generic.DeleteView):
    model = LearningObjective
    template_name = 'task_manager/confirm_delete_learning_objective.html'
   
    def get_object(self, queryset = ...):
        learning_objective_id = self.kwargs['learning_objective_id']
        return get_object_or_404(
            LearningObjective,
            user=self.request.user,
            id=learning_objective_id,
        )
    
    def get_success_url(self):
        category_id = self.object.category.id
        messages.success(self.request, '削除しました。')
        return reverse('task_manager:learning_objective_list', kwargs={'category_id': category_id})


# ========== 学習タスク ==========
# リスト表示
class LearningTaskListView(LoginRequiredMixin, generic.ListView):
    model = LearningMainTopic
    template_name = 'task_manager/learning_task_list.html'


    def get_queryset(self):

        # 学習目標idをURLから取得
        learning_objective_id = self.kwargs['learning_objective_id']

        return LearningMainTopic.objects.filter(
            user=self.request.user,
            learning_objective__id=learning_objective_id,
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 学習目標の取得
        learning_objective = get_object_or_404(
            LearningObjective, 
            id=self.kwargs['learning_objective_id']
        )
        context['learning_objective'] = learning_objective

        # main_topicの取得
        main_topics = LearningMainTopic.objects.filter(
            user=self.request.user, 
            learning_objective=learning_objective
        )
        
        # 各main_topicに紐づくsub_topicを全て取得してリストに追加
        sub_topics = LearningSubTopic.objects.filter(
            main_topic__in=main_topics
        )
        context['sub_topics'] = sub_topics

        return context
