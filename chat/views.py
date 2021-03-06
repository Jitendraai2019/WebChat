from django.shortcuts import render
from . models import Message, Room
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
import requests


@login_required(login_url='/login')
def user_details(request, username):
    ''''''
    username = request.user
    user_rooms = Room.objects.filter(participants__username=username)
    current_user = User.objects.get(username=username)
    all_users = User.objects.order_by('username')

    context = {
        'username': current_user,
        'room_deatails': filter_rooms_and_friends(user_rooms, current_user),
        'all_users': all_users
    }
    
    if request.method == "POST":
        print('*********testing*********')
        room_name = request.POST['room_name']
        print('*********testing*********')
        participants = request.POST.getlist('room-participants')
        print('*********testing*********')
        print('-------------------->>>>>', participants)
        # participants = participants.split()
        participants.append(current_user)
        print(participants)
        current_user = User.objects.get(username=username)
        room = Room.objects.filter(room_name=room_name)
        if not room:
            user = User.objects.get(username=username)
            new_room = Room.objects.create(room_name=room_name, user=user)
            new_room.save()

            for participant in participants:
                try:
                    temp = User.objects.get(username=participant)
                except:
                    temp = User.objects.create(username=participant)
                    temp.save()
                all_user = User.objects.all()
                
                if temp in all_user:
                    new_room.participants.add(temp)
                else:
                    new_user = User.objects.create(username=participant)
                    new_user.save()
                    new_room.participant.add(new_user)
            participants = new_room.participants.all()

            return redirect('chat:chat_rooms', username, new_room.room_name)

    return render(request, 'chat/user.html', context)


@login_required(login_url='/login')
def get_rooms(request, username):
    ''''''
    username = request.user
    current_user = User.objects.get(username=username)
    user_rooms = Room.objects.filter(participants__username=current_user)
    room_details = filter_rooms_and_friends(user_rooms, current_user)

    context = {
        'username': current_user,
        'rooms_details': room_details,
        'room_name': ' '
    }

    if request.method == "POST":
        room_search = request.POST['room_name']
        response = requests.get(f"http://127.0.0.1:8000/api/chat/{username}/{room_search}")
        
        if response.status_code == 200:
            friends = []
            rooms = []
            for room in response.json():
                print(room)
                rooms.append(room['room_name'])
                participants = get_friends(current_user, room['participants'])
                friends.append(participants)

            for room, friend in zip(rooms, friends):
                print(room, friend)
            
            context = {
                'username': current_user.username,
                'rooms_details': zip(rooms, friends),
                'room_name': ' '
            }
            
    return render(request, 'chat/room.html', context)


@login_required(login_url='/login')
def chat_rooms(request, username, room_name):
    ''''''
    username = request.user
    current_user = User.objects.get(username=username)
    user_rooms = Room.objects.filter(participants__username=current_user)
    room_deatails = filter_rooms_and_friends(user_rooms, current_user)
    room = Room.objects.get(room_name=room_name)

    participants = room.participants.all()
    participants_name = filter_participants(current_user, participants)
    is_participant_user = User.objects.get(username=current_user)

    if is_participant_user in participants:
        print("The current user is allowed to send message")
        messages = Message.objects.filter(room=room).order_by('-timestamp').all()

        if request.method == 'POST':
            msg = request.POST['chat-msg-input']
            data = Message(author=current_user, content=msg, room=room)
            data.save()
            return redirect('chat:chat_rooms', username, room.room_name)

        return render(request, 'chat/room.html', {
            'room_name': room_name,
            'username': current_user,
            'messages': reversed(messages),
            'rooms_details': room_deatails,
            'participants': participants_name,
            'group_name': ''
        })
    else:
        print("The current use user is not allowed to send message.")
        return HttpResponse("<h1>You are an unauthorized user for this room.</h1>")


def filter_rooms_and_friends(user_rooms, current_user):
    ''''''
    all_rooms = []
    participants = []
    for room in user_rooms:
        all_rooms.append(room.room_name)
        participants.append(room.participants.all())

    friends = []
    for users in participants:
        if len(users) == 2:
            for user in users:
                if user.username != current_user.username:
                    friends.append(user.username)
        else:
            temp = ''
            for user in users:
                temp += ' ' + user.username
            friends.append(temp)
    
    print(len(all_rooms), len(friends))
    return zip(all_rooms, friends)


def filter_participants(current_user, participants):
    '''
    parameters:
        participants (QuerySET): All participants of a room.
    '''
    friend_name = ''
    group_name = ""
    if len(participants) == 2:
        for participant in participants:
            if participant != current_user:
                friend_name = participant.username
        return friend_name
    else:
        for participant in participants:
            group_name += ' ' + participant.username
        return group_name


@login_required(login_url='/login')
def update_room(request, username, room_name):
    ''''''
    current_user = User.objects.get(username=username)
    return HttpResponse('Hello! I am an updation of room.')


@login_required(login_url='/login')
def delete_room(request, username, room_name):
    '''
    '''
    current_user = User.objects.get(username=username)
    room_name = Room.objects.get(room_name=room_name)
    temp = room_name.participants.all()
    room_name.participants.remove(current_user)
    
    return redirect('chat:get_rooms', current_user.username)


def get_friends(current_user, participants):
    ''''''
    print(current_user, type(current_user))
    friends = ''
    for user_id in participants:
        friend = User.objects.get(id=user_id)
        if friend != current_user:
            friends += ' ' + friend.username

    return friends