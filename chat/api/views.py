from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

from django.core.serializers.json import DjangoJSONEncoder
import json

from django.core.serializers import serialize

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
 

# @api_view(['GET', ])
# def api_search_room(request, room_name):
#     ''''''
#     try:
#         room_names = Room.objects.filter(room_name__contains=room_name)
#     except Room.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         # serializer = RoomSerializer(room_name)
#         # return Response(serializer.data)
#         # serialized = serialize('json', room_name)
#         serialized = json.dumps(list(room_names), cls=DjangoJSONEncoder)
#         return Response(serialized)