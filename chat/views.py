from django.shortcuts import render
from . models import Message, Room
from users.views import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# Create your views here.


@login_required(login_url='/login')
def user_details(request):
    username = request.user
    
    rooms = Room.objects.filter(user=username)
    print('-----------------', rooms)
    context = {
        'user': username,
        'rooms': rooms
    }
    if request.method == "POST":
        room_name = request.POST['room_name']
        return redirect('http://127.0.0.1:8000/chat/<str:room_name>/')
    return render(request, 'chat/user.html', context)


@login_required(login_url='/login')
def chat_rooms(request, room_name):

    current_user = request.user

    if request.method == 'POST':
        
        pass
    current_user = request.user
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': current_user

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