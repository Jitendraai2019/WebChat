from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

from chat.api.serializers import RoomSerializer
from chat.models import Room


@api_view(['GET', ])
def api_search_room(request, room_name):
    ''''''
    try:
        room_name = Room.objects.get(room_name=room_name)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = RoomSerializer(room_name)
        return Response(serializer.data)