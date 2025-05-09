from django.urls import path

from . import views


app_name = 'task_manager'
urlpatterns = [
    # Top画面
    path('', views.IndexView.as_view(), name='index'),
    # 問い合わせフォーム
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    # 興味カテゴリ
    path('interest_category_list/', views.InterestCategoryListView.as_view(), name='interest_category'),
    path('add_interest_category/', views.AddInterestCategoryView.as_view(), name='add_interest_category'),
    path('delete_interest_category/<int:category_id>/', views.DeleteInterestCategory.as_view(), name='delete_interest_category'),
    # 学習目標
    path('learning_objective_list/<int:category_id>/', views.LearningObjectiveListView.as_view(), name='learning_objective_list'),
    path('setting_learning_objective/<int:category_id>/', views.SettingLearningObjectiveView.as_view(), name='setting_learning_objective'),
    path('preview_generated_task/', views.PreviewGeneratedTask.as_view(), name='preview_generated_task'),
    path('save_learning_task/<int:category_id>', views.SaveLearningTask.as_view(), name='save_learning_task'),
    path('delete_learning_objective/<int:learning_objective_id>/', views.DeleteLerningObjectiveView.as_view(), name='delete_learning_objective'),
    # 学習タスク
    path('learning_task_list/<int:learning_objective_id>/', views.LearningTaskListView.as_view(), name='learning_task_list'),
]
