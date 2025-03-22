from django.contrib.auth.models import AbstractUser
from django.db import models



# カスタムユーザー
class CustomUser(AbstractUser):
    interest_categories = models.ManyToManyField(
        'task_manager.Category',
        through='task_manager.UserInterestCategory',
        related_name='interested_users',
        )


    class Meta:
        verbose_name_plural = 'CustomUser'
