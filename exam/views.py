from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View, generic
from django.shortcuts import render, get_object_or_404

from ai_support.ai_survices import generate_multipul_choice_question
from task_manager.models import LearningObjective, LearningMainTopic, LearningSubTopic


# 選択問題
class MultipleChoiceQuestionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name

        # セッションのスコアを初期化
        request.session['total_score'] = 0

        # 出題する問題のトピックidを取得、セッションに保存
        topic_id = self.kwargs['topic_id']
        if 'main' in url_name:
            # トピックオブジェクト取得
            main_topic = get_object_or_404(LearningMainTopic, id=topic_id)
            sub_topics = main_topic.sub_topics.all()

            # セッションに保存(トピックid)
            main_topic_id = main_topic.id
            sub_topic_ids = list(sub_topics.values_list('id', flat=True))
            request.session['main_topic_id'] = main_topic_id
            request.session['sub_topic_ids'] = sub_topic_ids

            # 問題生成
            sub_topics_str = ', '.join([sub.sub_topic for sub in sub_topics])
            question = generate_multipul_choice_question(title=sub_topics_str)

        elif 'sub' in url_name:
            # セッションに保存(トピックid)
            sub_topic = get_object_or_404(LearningSubTopic, id=topic_id)
            main_topic = sub_topic.main_topic
            request.session['main_topic_id'] = main_topic.id
            request.session['sub_topic_id'] = sub_topic.id

            # 問題生成
            question = generate_multipul_choice_question(title=sub_topic.sub_topic)
        

        # セッションに保存(学習目標id、生成された問題)
        learning_objective_id = main_topic.learning_objective.id
        request.session['learning_objective_id'] = learning_objective_id

        if question:
            request.session['question'] = question
        else:
            context = {'message': '問題の生成に失敗しました。再度お試しください。'}
            return render(request, 'exam/question_error.html', context)


        context = {
            'learning_objective_id': learning_objective_id,
            'question': question,
        }
        return render(request, 'exam/exam.html', context)


    def post(self, request, *args, **kwargs):
        # セッションから取得(問題、問題数、総獲得スコア)
        question = request.session.get('question')
        question_count = request.session.get('question_count', 1)
        total_score = request.session.get('total_score', 0)
        
        # ユーザーの回答を取得
        answer = request.POST.get('')


# 記述問題
class ConstructedQuestionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        pass


# 総合問題
class IntegratedQuestionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
