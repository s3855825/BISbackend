from django.urls import path

from . import views


url_patterns = [
    path('', views.GroupView.as_view(), name='groups_all'),
    path('<int:pk>/', views.GroupDetailView.as_view(), name='groups_details'),
    path('<int:pk>/members/', views.GroupMemberView.as_view(), name='groups_members_all'),
    path('<int:pk>/tasks/', views.GroupTaskView.as_view(), name='groups_tasks_all'),
    path('<int:pk>/tasks/<int:pk>/', views.GroupTaskDetailView.as_view(), name='group_tasks_details'),
]
