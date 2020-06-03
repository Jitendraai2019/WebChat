from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='user_logout')
]