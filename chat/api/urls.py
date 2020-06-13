from django.urls import path
from chat.api.views import RoomApiView

app_name = 'room_api'

urlpatterns = [
    # path('<str:room_name>/', api_search_room, name='api_search_room'),
    path('<str:username>/<str:search_field>/', RoomApiView.as_view(), name='api_search_room'),
    # path('rooms/', ApiRoomListView.as_view, name="search_room")
]