from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/<str:username>/', views.user_details, name='user_details'),
    path('chat/<str:username>/rooms/', views.chat_rooms, name='all_rooms'),
    path('chat/<str:username>/rooms/<str:room_name>/', views.chat_rooms, name='chat_rooms')
]
