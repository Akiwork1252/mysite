from django.urls import path

from . import views


app_name = 'task_manager'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inquiry/', views.InquiryView.as_view(), name='inquiry'),
    path('interest_category_list/', views.InterestCategoryListView.as_view(), name='interest_category'),
    path('add_interest_category/', views.AddInterestCategoryView.as_view(), name='add_interest_category'),
    path('delete_interest_category/<int:category_id>/', views.DeleteInterestCategory.as_view(), name='delete_interest_category'),
]
