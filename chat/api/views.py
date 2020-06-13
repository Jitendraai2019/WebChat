from rest_framework import status
from rest_framework.response import Response 
from rest_framework.decorators import api_view

# from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter, OrderingFilter

from django.core.serializers.json import DjangoJSONEncoder
import json

from django.core.serializers import serialize

from chat.api.serializers import RoomSerializer
from chat.models import Room
from django.contrib.auth.models import User


class RoomApiView(APIView):
    ''''''

    def get_queyset(self, username, search_field):
        ''''''
        all_rooms = Room.objects.all()
        all_users = User.objects.all()
        queryset = Room.objects.filter(room_name__contains=search_field).filter(participants__username=username)
        print(queryset)
        return queryset


    def get(self, request, username, search_field):
        print('**************api searching**********************')
        queryset = self.get_queyset(username, search_field)
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

    # queryset = Room.objects.all()
    # serializer_class = RoomSerializer
    # filter_backends = (SearchFilter, OrderingFilter)
    # search_fields = ('room_name', 'participants__username')
    # authentication_classes = 

    pass



# @api_view(['GET', ])
# def api_search_room(request, room_name):
#     ''''''
#     try:
#         room_name = Room.objects.get(room_name=room_name)
#     except Room.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = RoomSerializer(room_name)
#         return Response(serializer.data)
 

# @api_view(['GET', ])
# def api_search_room(request, room_name):
#     ''''''
#     try:
#         room_names = Room.objects.filter(room_name__contains=room_name)
#     except Room.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
    
#     if request.method == 'GET':
#         serializer = RoomSerializer(room_names, many=True)
#         return Response(serializer.data)