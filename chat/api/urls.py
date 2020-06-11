from django.urls import path
from chat.api.views import api_search_room 

app_name = 'room_api'

urlpatterns = [
    path('<str:room_name>/', api_search_room, name='api_search_room'),
]