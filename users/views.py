from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout



# Create your views here.


def index(request):
    return render(request, 'users/signup.html')


def signup(request):
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
            return redirect('http://127.0.0.1:8000/login/')

    return render(request, 'users/index.html')


def user_login(request):
    ''''''
    if request.method == 'POST':
        print('++++++++++++++++++++++++++++++')
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print('cheking user name-------> ', user)
        print('++++++++++++++++++++++++++++++')

        if user is not None:
            login(request, user)
            return redirect('http://127.0.0.1:8000/chat/')
        # else:
        #     return redirect('http://127.0.0.1:8000/login/')
    return render(request, 'users/login.html')
    # return HttpResponse("Hello, I am a login page.")


def user_logout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')
    # return render('users/index.html')
