from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/', views.user_details, name='user_details'),
    path('chat/<str:room_name>/', views.chat_rooms, name='chat_room')
]
