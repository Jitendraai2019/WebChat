from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


# Create your models here.
class Room(models.Model):
    user = models.ForeignKey(
            User, on_delete=models.CASCADE
        )
    room_name = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name


class Message(models.Model):
    author = models.ForeignKey(
            User, related_name='author_messages', on_delete=models.CASCADE
        )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username
