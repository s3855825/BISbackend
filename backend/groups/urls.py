from django.urls import path

from . import views


urlpatterns = [
    path('', views.GroupView.as_view(), name='groups_all'),
    path('<int:pk>/', views.GroupDetailView.as_view(), name='groups_details'),
    path('<int:pk>/members/', views.GroupMemberView.as_view(), name='groups_members_all'),
    path('<int:pk>/tasks/', views.GroupTaskView.as_view(), name='groups_tasks_all'),
]
