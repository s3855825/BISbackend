from django.urls import path

from . import views

url_patterns = [
    path('', views.PostView.as_view(), name='posts_all'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_details'),
]