from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserView.as_view(), name='users_all'),
    path('<int:primary_key>/', views.UserDetailView.as_view(), name='users_details'),
    path('auth/', views.UserAuthView.as_view(), name='users_auth'),
    path('<int:primary_key>/posts/', views.UserPostView.as_view(), name='users_post'),
    path('<int:primary_key>/groups/', views.UserGroupView.as_view(), name='users_group'),
    path('<int:primary_key>/review/', views.UserReviewView.as_view(), name='users_review'),
]
