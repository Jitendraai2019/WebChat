from rest_framework import serializers
from chat.models import Room


class RoomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Room
        fields = ['user', 'room_name', 'participants']
    