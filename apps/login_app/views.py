from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from apps.login_app.models import *
import bcrypt

def index(request):
    return render(request, "login_app/index.html")


def register(request):
    if request.method == "GET":
        return redirect(reverse('login:index'))
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    password = request.POST['password_reg']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email_reg'], password=pw_hash, birthday=request.POST['birthday'])
    request.session['user_id'] = new_user.id
    return redirect(reverse('wall:index'))

def login(request):
    if request.method == "GET":
        return redirect(reverse('login:index'))
    user = User.objects.filter(email__iexact=request.POST['email'])
    errors = User.objects.login_validator(request.POST, user)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    request.session['user_id'] = user[0].id
    return redirect(reverse('wall:index'))


def logout(request):
    request.session.flush()
    return redirect('/')