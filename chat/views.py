from django.shortcuts import render
from . models import Message, Room
from users.views import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
# Create your views here.


@login_required(login_url='/login')
def user_details(request):
    username = request.user
    rooms = Room.objects.filter(user=username)
    context = {
        'user': username,
        'rooms': rooms
    }
    if request.method == "POST":
        room_name = request.POST['room_name']
        room = Room.objects.filter(room_name=room_name)
        if not room:
            user = User.objects.get(username=username)
            new_room = Room.objects.create(room_name=room_name, user=user)
            new_room.save()
        # return reverse('chat:chat_room')
        return redirect('http://127.0.0.1:8000/chat/' + room_name + '/')

    return render(request, 'chat/user.html', context)


@login_required(login_url='/login')
def chat_rooms(request, room_name):
    ''''''
    current_user = request.user
    user_all_rooms = Room.objects.filter(user=current_user)
    rooms = Room.objects.get(room_name=room_name)
    messages = Message.objects.filter(room=rooms).order_by('-timestamp').all()[:6]
    # messages = messages.order_by('-timstamp').all()[:10]

    if request.method == 'POST':
        msg = request.POST['chat-msg-input']
        print(msg)
        print(room_name)
        data = Message(author=current_user, content=msg, room=rooms)
        # data = Message.objects.create(author=current_user, content=msg, room=rooms)
        # print('--------->',data, type(data))
        data.save()
        return redirect('http://127.0.0.1:8000/chat/' + room_name + '/')

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': current_user,
        'messages': messages,
        'user_all_rooms': user_all_rooms
    })




# @login_required(login_url='/login')
# def chat_room(request):
#     ''''''
#     messages = Message.objects.all()
#     print(messages)
#     current_user = request.user
#     context = {
#         'messages': messages,
#         'user': current_user
#     }
#     print(current_user)
#     # print('--------------------------')
#     # for msg in messages:
#     #     print(msg)
#     #     print(msg.user)
#     # print('---------------------------')
#     if request.method == 'POST':
#         message = request.POST['message']
#         print('*********', message)
#         data = Message(user=current_user, message=message)
#         data.save()
#         return redirect('http://127.0.0.1:8000/chat/')

#     return render(request, 'chat/room.html', context)