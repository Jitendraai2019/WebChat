# DataBase Models
------------------
## Room
--------
    user = models.ForeignKey(
            User, on_delete=models.CASCADE
        )
    room_name = models.CharField(max_length=50)
    participants = models.ManyToManyField(User, related_name='friends', blank=True)

## Message
----------
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

# URL Designing
---------------
1. Signup            -    /signup/
2. Login             -     /login/
3. Logout            -     /logout/
4. After user Login  -     /chats/
5. All Chat Rooms    -     /chats/<str:room_name>/messages