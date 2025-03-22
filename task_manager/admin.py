from django.contrib import admin

from .models import Category, UserInterestCategory, LearningObjective, LearningMainTopic, LearningSubTopic


# Register your models here.
admin.site.register(Category)
admin.site.register(UserInterestCategory)
admin.site.register(LearningObjective)
admin.site.register(LearningMainTopic)
admin.site.register(LearningSubTopic)
