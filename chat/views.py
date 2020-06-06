from django.shortcuts import render
from . models import Message, Room
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse


@login_required(login_url='/login')
def user_details(request):
    ''''''
    username = request.user
    # print(username, type(username))
    user_rooms = Room.objects.filter(participants__username=username)
    # print("------------->", user_rooms)
    current_user = User.objects.get(username=username)
    context = {
        'user': username,
        'room_deatails': filter_rooms_and_friends(user_rooms, current_user)
    }
    if request.method == "POST":
        room_name = request.POST['room_name']
        participants = request.POST['room-participants']
        participants = participants.split()
        # print('------------>',participants)

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
            # print('-----------')
            room = Room.objects.filter(room_name=room_name)
            if not room:
                user = User.objects.get(username=username)
                # print('I am new room.', room_name, user, type(user))
                new_room = Room.objects.create(room_name=room_name, user=user)
                new_room.save()

                for participant in participants:
                    # print('In for loop')
                    try:
                        temp = User.objects.get(username=participant)
                        print(temp)
                    except:
                        temp = User.objects.create(username=participant)
                        temp.save()
                        # print(temp)
                    all_user = User.objects.all()
                    
                    if temp in all_user:
                        new_room.participants.add(temp)
                    else:
                        new_user = User.objects.create(username=participant)
                        new_user.save()
                        new_room.participant.add(new_user)
                participants = new_room.participants.all()
                print('------------------------')
                print(participants)
                print('------------------------')

                return redirect('chat:chat_room', new_room.room_name)

    return render(request, 'chat/user.html', context)


@login_required(login_url='/login')
def chat_rooms(request, room_name):
    ''''''
    current_user = request.user
    current_user = User.objects.get(username=current_user)

    user_rooms = Room.objects.filter(participants__username=current_user)
    room_deatails = filter_rooms_and_friends(user_rooms, current_user)
    # print('------room_deatails--------------', room_deatails)
    room = Room.objects.get(room_name=room_name)

    participants = room.participants.all()
    is_participant_user = User.objects.get(username=current_user)

    if is_participant_user in participants:
        print("The current user is allowed to send message")
        messages = Message.objects.filter(room=room).order_by('-timestamp').all()

        if request.method == 'POST':
            msg = request.POST['chat-msg-input']
            data = Message(author=current_user, content=msg, room=room)
            data.save()
            return redirect('chat:chat_room', room.room_name)

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'username': current_user,
            'messages': reversed(messages),
            'rooms_details': room_deatails,
            'participants': '',
            'group_name': ''
        })
    else:
        print("The current use user is not allowed to send message.")
        return HttpResponse("<h1>You are an unauthorized user for this room.</h1>")


def filter_rooms_and_friends(user_rooms, current_user):
    ''''''
    all_rooms = []
    participants = []
    # print('------------------------')
    # print('<--------user room-------->', user_rooms)
    # print('-----------------------')
    for room in user_rooms:
        all_rooms.append(room.room_name)
        # print(room.room_name, type(room.room_name))
        participants.append(room.participants.all())

    friends = []
    # print('-------participands length-------->', len(participants), len(user_rooms))
    print('*************************')
    print(participants)
    # participants = set(participants)
    print(len(participants))
    print('***********************')
    for users in participants:
        # print('-------------------')
        print(len(users))
        if len(users) == 2:
            for user in users:
                if user.username != current_user.username and user.username not in friends:
                    # print(user.username)
                    friends.append(user.username)
        elif len(users) >= 3:
            temp = ''
            for user in users:
                # if user.username != current_user.username and user.username not in friends:
                    # print(user.username)
                temp += ' ' + user.username
            friends.append(temp)

    # print(friends)
    # print('------all_romms---', all_rooms)
    print(len(all_rooms), len(friends))
    return zip(all_rooms, friends)
