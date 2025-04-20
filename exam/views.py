from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View, generic
from django.shortcuts import render, get_object_or_404

from ai_support.ai_survices import (
    generate_multipul_choice_question,
    generate_constructed_question,
    generate_integrated_question,
    grade_multiple_choice_question,
    grade_constructed_question,
)
from analysis.models import Progress
from task_manager.models import LearningObjective, LearningMainTopic, LearningSubTopic


# 選択問題(5問出題)
class MultipleChoiceQuestionsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name

        # セッションを初期化(スコア、問題履歴、問題数、出題問題)
        for key in ['totol_score', 'question_history', 'question_count', 'current_question']:
            request.session.pop(key, None)

        # 出題する問題のトピックidを取得、セッションに保存
        topic_id = self.kwargs['topic_id']
        if 'main' in url_name:
            # トピックオブジェクト取得
            main_topic = get_object_or_404(LearningMainTopic, id=topic_id)
            sub_topics = main_topic.sub_topics.all()

            # セッションに保存(メイントピックid、関連サブトピックid)
            main_topic_id = main_topic.id
            sub_topic_ids = list(sub_topics.values_list('id', flat=True))
            request.session['main_topic_id'] = main_topic_id
            request.session['sub_topic_ids'] = sub_topic_ids

            # 問題生成
            sub_topics_str = ', '.join([sub.sub_topic for sub in sub_topics])
            question = generate_multipul_choice_question(title=sub_topics_str)

            topic_name = main_topic.main_topic

        elif 'sub' in url_name:
            # セッションに保存(サブトピックid)
            sub_topic = get_object_or_404(LearningSubTopic, id=topic_id)
            main_topic = sub_topic.main_topic
            request.session['main_topic_id'] = main_topic.id
            request.session['sub_topic_id'] = sub_topic.id

            # 問題生成
            question = generate_multipul_choice_question(title=sub_topic.sub_topic)

            topic_name = sub_topic.sub_topic

        # セッションに保存(学習目標id、生成された問題)
        learning_objective_id = main_topic.learning_objective.id
        learning_objective = get_object_or_404(LearningObjective, id=learning_objective_id)
        request.session['learning_objective_id'] = learning_objective_id

        if question:
            # セッションに保存(1問目、問題リスト、総スコア、問題数カウント)
            request.session['current_question'] = question  # 採点で使用

            history = request.session.get('question_history', [])
            history.append(question)
            request.session['question_history'] = history

            request.session['total_score'] = 0
            request.session['question_count'] = 1
        else:
            context = {'message': '問題の生成に失敗しました。再度お試しください。'}
            return render(request, 'exam/question_error.html', context)


        context = {
            'learning_objective': learning_objective,
            'question': question,
            'topic': topic_name,
            'topic_id': topic_id,
            'url_name': f'exam:{url_name}',
        }
        return render(request, 'exam/exam.html', context)


    def post(self, request, *args, **kwargs):
        url_name = request.resolver_match.url_name

        # セッションから取得(出題問題)
        question = request.session.get('current_question')
        
        # ユーザーの回答を取得
        answer = request.POST.get('answer')

        # 採点結果を取得
        try:
            scoring_result = grade_multiple_choice_question(question, answer)
            score = scoring_result['score']
            explanation = scoring_result['explanation']
        except (ValueError, KeyError) as e:
            score = 0.0
            explanation = '採点中にエラーが発生しました。'

        # セッション更新(総スコア、問題数カウント)
        request.session['total_score'] += score
        request.session['question_count'] += 1
        total_score = request.session.get('total_score')
        question_count = request.session.get('question_count')

        # レスポンスデータ
        response_data = {
            'score': score,
            'explanation': explanation,
            'total_score': total_score,
            'question_count': question_count,
        }

        # 次の問題
        if question_count <= 5:
            # 出題履歴を取得
            history = request.session.get('question_history', [])
            print(f'history: {history}')
            if 'main' in url_name:
                sub_topic_ids = request.session.get('sub_topic_ids')
                # 問題生成
                sub_topics = LearningSubTopic.objects.filter(id__in=sub_topic_ids)
                sub_topics_str = ', '.join([sub.sub_topic for sub in sub_topics])
                question = generate_multipul_choice_question(title=sub_topics_str, previous_questions=history)
            elif 'sub' in url_name:
                sub_topic_id = request.session.get('sub_topic_id')
                # 問題生成
                sub_topic = get_object_or_404(LearningSubTopic, id=sub_topic_id)
                question = generate_multipul_choice_question(title=sub_topic.sub_topic, previous_questions=history)

            # 生成した問題を履歴に追加
            history.append(question)
            request.session['question_history'] = history

            # レスポンスデータに次の問題を追加
            response_data.update({
                'next_question': question,
            })

        # 終了
        else:
            # Progressモデル保存データを取得(学習目標、メイントピック、サブトピック)
            learning_objective_id = request.session.get('learning_objective_id')
            learning_objective = get_object_or_404(LearningObjective, id=learning_objective_id)
            main_topic_id = request.session.get('main_topic_id')
            main_topic = get_object_or_404(LearningMainTopic, id=main_topic_id)
            if 'main' in url_name:
                sub_topic_ids = request.session.get('sub_topic_ids')
                sub_topic = get_object_or_404(LearningSubTopic, id=sub_topic_ids[0])
            elif 'sub' in url_name:
                sub_topic_id = request.session.get('sub_topic_id')
                sub_topic = get_object_or_404(LearningSubTopic, id=sub_topic_id)
            
            # Progressモデルにテストデータを保存
            progress = Progress.objects.create(
                user=request.user,
                learning_objective=learning_objective,
                main_topic=main_topic,
                sub_topic=sub_topic,
                score=total_score,
                session_type='main' if 'main' in url_name else 'sub',
            )

            # LearningObjectiveモデルの総獲得スコアを更新
            learning_objective.total_score = (learning_objective.total_score or 0) + total_score
            learning_objective.save()

            response_data.update({
                'finished': True,
                'message': '全5問終了しました。終了ボタンを押してください。お疲れ様でした。',
            })

        return JsonResponse(response_data)


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
