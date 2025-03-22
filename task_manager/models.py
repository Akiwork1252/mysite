from django.db import models

from accounts.models import CustomUser


# カテゴリリスト
class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    

# 中間モデル(CustomUser, Category)
class UserInterestCategory(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')  # 同じカテゴリを重複登録しない


# 学習目標
class LearningObjective(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    current_level = models.CharField(max_length=50, blank=True, null=True)
    target_level = models.TextField(blank=True, null=True)
    total_score = models.IntegerField(blank=True, null=True)
    target_study_time = models.FloatField(blank=True, null=True, help_text='目標学習時間 (h)')
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def actual_study_time(self):
        return self.progresses.aggregate(
            total=models.Sum('time_spent')
        )['total'] or 0

    def __str__(self):
        return self.title
    

# 学習メイントピック
class LearningMainTopic(models.Model):
    STATUS = [
        ('incomplete', '未完了'),
        ('completed', '完了')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    learning_objective = models.ForeignKey(LearningObjective, on_delete=models.CASCADE)
    main_topic = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    status = models.CharField(
        choices=STATUS,
        default='incomplete',
    )

    def __str__(self):
        return self.main_topic


# 学習サブトピック
class LearningSubTopic(models.Model):
    STATUS = [
        ('incomplete', '未完了'),
        ('completed', '完了') 
    ]

    main_topic = models.ForeignKey(
        LearningMainTopic, 
        related_name='sub_topics', 
        on_delete=models.CASCADE
    )
    sub_topic = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    estimated_time = models.FloatField(blank=True, null=True, help_text='推定学習時間 (h)')
    status = models.CharField(
        choices=STATUS,
        default='incomplete'
    )

    def __str__(self):
        return f'{self.main_topic.main_topic} - {self.sub_topic}'
