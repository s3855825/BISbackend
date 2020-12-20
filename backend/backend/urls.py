"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from accounts.views import UserView, UserAuthView, UserDetailView
from django.contrib import admin
from django.urls import path, include
from groups.views import GroupView, GroupDetailView, TaskView, GroupTaskView, GroupMemberView, TasksMemberViews
from posts.views import PostView, PostDetailView

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', UserView.as_view(), name='users'),
    path('accounts/<int:pk>/', UserDetailView.as_view(), name='user_details'),
    path('accounts/auth/', UserAuthView.as_view(), name='auth'),

    path('posts/', PostView.as_view(), name='posts'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_details'),

    path('groups/', GroupView.as_view(), name='groups'),
    path('groups/<int:pk>', GroupDetailView.as_view(), name='group_details'),
    path('groups/<int:pk>/tasks/', GroupTaskView.as_view(), name='group_tasks'),
    path('groups/<int:pk>/tasks/<int:pk>', TaskView.as_view(), name='task_details'),
    path('groups/')
]
