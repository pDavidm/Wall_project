from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 charaters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at leat 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_reg']):             
            errors['email'] = "Invalid email address"
        if len(User.objects.filter(email__iexact=postData['email_reg'])) > 0:
            errors['email'] = "Email already in use"
        if len(postData['password_reg']) < 8 or len(postData['password_reg']) > 14:
            errors['password'] = "Password must be between 8 and 14 characters"
        if postData['password_reg'] != postData ['confirm_pw']:
            errors['password'] = "Passwords do not match"
        try:
            today = datetime.date.today()
            b_day = datetime.datetime.strptime(postData['birthday'], '%Y-%m-%d')
            if (today.year - b_day.year - ((today.month, today.day)<(b_day.month, b_day.day))) < 13:
                errors['birthday'] = "User must be at least 13 years old"
        except:
            errors['birthday'] = "Invalid date"
        return errors

    def login_validator(self, postData, user):
        errors = {}
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors['password'] = "Incorrect password!"
        else:
            errors['email'] = 'Email does not exsist'
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()