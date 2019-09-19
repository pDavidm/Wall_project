from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from apps.login_app.models import User
from apps.wall_app.models import *
from datetime import datetime, timedelta
import bcrypt

def index(request):
    if not 'user_id' in request.session:
        return redirect(reverse('login:index'))
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'post_list': Post.objects.all().order_by('-created_at')
        }
        return render(request, "wall_app/index.html", context)


def makePost(request):
    if request.method == "GET":
        return redirect(reverse('wall:index'))
    errors = Post.objects.post_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(reverse('wall:index'))
    Post.objects.create(post=request.POST['post'], user=User.objects.get(id=request.session['user_id']))
    return redirect(reverse('wall:index'))

def makeComment(request):
    if request.method == "GET":
        return redirect(reverse('wall:index'))
    errors = Comment.objects.post_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(reverse('wall:index'))
    parent_post = Post.objects.get(id=request.POST['post_id'])
    Comment.objects.create(comment=request.POST['comment'], user=User.objects.get(id=request.session['user_id']), post=parent_post)
    return redirect(reverse('wall:index'))

def deletePost(request):
    if request.method == "GET":
        return redirect(reverse('wall:index'))
    user = User.objects.get(id=request.session['user_id'])
    errors = Post.objects.delete_validator(request.POST, user)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(reverse('wall:index'))
    post = Post.objects.get(id=request.POST['post_id'])
    post.delete()
    return redirect(reverse('wall:index'))


