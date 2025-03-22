from django.db import models

from accounts.models import CustomUser
from task_manager.models import LearningObjective, LearningMainTopic, LearningSubTopic


# 学習進捗
class Progress(models.Model):
    SESSION_TYPE_CHOICES = [
        ('objective', '総合テスト'),
        ('main', 'メイントピック'),
        ('sub', 'サブトピック'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    learning_objective = models.ForeignKey(
        LearningObjective, 
        related_name='progresses',
        blank=True, null=True, on_delete=models.CASCADE)
    main_topic = models.ForeignKey(LearningMainTopic, blank=True, null=True, on_delete=models.CASCADE)
    sub_topic = models.ForeignKey(LearningSubTopic, blank=True, null=True, on_delete=models.CASCADE)
    score = models.FloatField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    time_spent = models.FloatField(blank=True, null=True, help_text='このセッションでの学習時間 (h)')
    session_type = models.CharField(
        max_length=20,
        choices=SESSION_TYPE_CHOICES,
        default='sub',
        )

    def __str__(self):
        return f'{self.user} | {self.score} | {self.date}'
