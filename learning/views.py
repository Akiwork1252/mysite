from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.urls import reverse

from ai_support.ai_survices import lectures_by_ai
from task_manager.models import LearningSubTopic


# Create your views here.
class LearningView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        learning_topic_id = self.kwargs['learning_topic']
        learning_topic = get_object_or_404(LearningSubTopic, id=learning_topic_id)

        # AIによる講義を生成
        ai_lecture = lectures_by_ai(learning_topic.sub_topic)

        # 講義内容をセッションに保存
        request.session['ai_lecture'] = ai_lecture

        context = {
            'learning_topic': learning_topic,
            'ai_lecture': ai_lecture
            }
        
        return render(request, 'learning/learning.html', context)


    def post(self, request, *args, **kwargs):
        # ユーザーの入力を受け取る
        user_input = request.POST.get('message', '')

        # 講義のオブジェクトを取得
        learning_topic_id = self.kwargs['learning_topic']
        learning_topic = get_object_or_404(LearningSubTopic, id=learning_topic_id)
        learning_objective_id = learning_topic.main_topic.learning_objective.id

        # チャット終了
        if user_input == '終了':
            return JsonResponse({'redirect_url': reverse(
                'task_manager:learning_task_list',
                kwargs={'learning_objective_id': learning_objective_id}
            )})
        
        # セッションから講義内容を取得
        lecture_contents = request.session.get('ai_lecture')

        # AIによる返答
        lecture_response = lectures_by_ai(title=learning_topic.sub_topic, user_input=user_input, lecture_contents=lecture_contents)

        return JsonResponse({'lecture_response': lecture_response})




