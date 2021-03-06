from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


def index(request):
    ''''''
    current_user = request.user
    return render(request, 'users/index.html', {'username': current_user})


def signup(request):
    '''
    '''
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        messages.success(request, 'you successfully signed up')
        print(username, email, password, confirm_password)

        if password == confirm_password:
            new_user = User.objects.create_user(username, email, password)
            new_user.save()
            return redirect('user:login')

    return render(request, 'users/signup.html', {})


def user_login(request):
    '''
    '''
    username = request.user
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('chat:get_rooms', username)

    return render(request, 'users/login.html', {'username': username})


def user_logout(request):
    logout(request)
    return redirect('user:home')
