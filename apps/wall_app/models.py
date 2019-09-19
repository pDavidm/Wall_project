from django.db import models
import re
import bcrypt
import datetime
from apps.login_app.models import User
from django.utils import timezone 


class PostManager(models.Manager):
    def post_validator(self, postData):
        errors = {}
        if len(postData['post']) == 0:
            errors['post'] = "empty post"
        return errors
    def delete_validator(self,postData, user):
        errors = {}
        try:
            post = Post.objects.get(id=postData['post_id'])
            if post.user.id != user.id:
                errors['delete'] = "Not your post!"
            if post.created_at + datetime.timedelta(minutes=30) < timezone.now():
                errors['delete'] = "Posts can only be deleted within 30 minuets of posting"
        except:
            errors['delete'] = "error"
        return errors

class CommentManager(models.Manager):
    def post_validator(self, postData):
        errors = {}
        if len(postData['comment']) == 0:
            errors['comment'] = "empty post"
        return errors

class Post(models.Model):
    post = models.TextField()
    user = models.ForeignKey(User, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PostManager()

class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(User, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()
