from django.shortcuts import render
from . models import Message, Room
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# from django.urls import reverse
from django.contrib.auth.models import User


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
        print('*************************')
        participants = request.POST['room-participants']
        print('----------->>>>>', participants, type(participants))
        participants = participants.split()
        print(participants)

        if len(participants) == 0:
            room = Room.objects.filter(room_name=room_name)
            if not room:
                user = User.objects.get(username=username)
                new_room = Room.objects.create(room_name=room_name, user=user)
                new_room.save()
                return redirect('chat:chat_room', new_room.room_name)
            return render(request, 'chat/user.html', context)
        else:
            current_user = User.objects.get(username=username)
            print('-----------')
            room = Room.objects.filter(room_name=room_name)
            if not room:
                user = User.objects.get(username=username)
                print('I am new room.', room_name, user, type(user))
                new_room = Room.objects.create(room_name=room_name, user=user)
                new_room.save()

                for participant in participants:
                    print('In for loop')
                    try:
                        temp = User.objects.get(username=participant)
                        print(temp)
                    except:
                        temp = User.objects.create(username=participant)
                        temp.save()
                        print(temp)
                    all_user = User.objects.all()
                    
                    if temp in all_user:
                        new_room.participants.add(temp)
                    else:
                        new_user = User.objects.create(username=participant)
                        new_user.save()
                        new_room.participant.add(new_user)
                participants = new_room.participants.all()
                print("participants", participants)
                return redirect('chat:chat_room', new_room.room_name)

    return render(request, 'chat/user.html', context)


@login_required(login_url='/login')
def chat_rooms(request, room_name):
    ''''''
    current_user = request.user
    user_all_rooms = Room.objects.filter(user=current_user)
    rooms = Room.objects.get(room_name=room_name)
    messages = Message.objects.filter(room=rooms).order_by('-timestamp').all()[:6]

    if request.method == 'POST':
        msg = request.POST['chat-msg-input']
        print(msg)
        print(room_name)
        data = Message(author=current_user, content=msg, room=rooms)
        data.save()
        return redirect('http://127.0.0.1:8000/chat/' + room_name + '/')

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': current_user,
        'messages': messages,
        'user_all_rooms': user_all_rooms
    })
