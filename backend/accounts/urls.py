from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserView.as_view(), name='users_all'),
    path('<int:pk>/', views.UserDetailView.as_view(), name='users_details'),
    path('auth/', views.UserAuthView.as_view(), name='users_auth'),
]
