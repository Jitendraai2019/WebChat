from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('chat/<str:username>/', views.user_details, name='user_details'),
    path('chat/<str:username>/rooms/', views.get_rooms, name='get_rooms'),
    path('chat/<str:username>/rooms/<str:room_name>/', views.chat_rooms, name='chat_rooms'),
    path('chat/<str:username>/rooms/<str:room_name>/update/', views.update_room, name='update_room'),
    path('chat/<str:username>/rooms/<str:room_name>/delete/', views.delete_room, name='delete_room'),
]
