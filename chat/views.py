from django.shortcuts import render
from . models import Message, Room
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
# from django.urls import reverse
from django.contrib.auth.models import User
from django.http import HttpResponse


@login_required(login_url='/login')
def user_details(request, username):
    ''''''
    username = request.user
    # print(username, type(username))
    user_rooms = Room.objects.filter(participants__username=username)
    # print("------------->", user_rooms)
    current_user = User.objects.get(username=username)
    context = {
        'username': current_user,
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
        # 'participants': participants_name,
    }
    # return HttpResponse('<h1>I am having all the rooms.</h1>')
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
            return redirect('chat:chat_room', room.room_name)

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
        print('-------------------')
        print(len(users))
        print(users)
        if len(users) == 2:
            for user in users:
                if user.username != current_user.username:
                    friends.append(user.username)
        else:
            temp = ''
            for user in users:
                temp += ' ' + user.username
            print(temp)
            friends.append(temp)
        print(len(friends))

    print(len(all_rooms), len(friends))
    print(friends)
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
    return HttpResponse('Hello! I am an updation of room.')


@login_required(login_url='/login')
def delete_room(request, username, room_name):
    ''''''
    return HttpResponse("Hello! I am to delete the room.")
