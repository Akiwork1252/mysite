from django.urls import path

from . import views


app_name = 'ai_support'
urlpatterns = [
    path('generate_choice_test/<int:topic_id>', views.generate_choice_test, name='generate_choice_test'),
]
