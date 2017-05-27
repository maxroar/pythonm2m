from __future__ import unicode_literals
import re
from django.db import models
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validate_reg(self, postData):
        # list to hold error messages
        errors = []
        if not len(postData['first_name']) > 2:
            errors.append('First name must be at least 3 characters.')
        if not len(postData['email']) > 2:
            errors.append('User name must be at least 3 characters.')
        if not len(postData['pass1']) > 7:
            errors.append('Password must be at least 8 characters.')
        if not postData['pass1'] == postData['pass2']:
            errors.append('Passwords must match.')
        if not self.check_email(postData):
            errors.append('User name already in use.')
        return errors

    def check_email(self, postData):
        emails = User.objects.filter(email=postData['email'])
        if emails:
            return False
        return True

    def create_user(self, postData):
        User.objects.create(first_name=postData['first_name'], last_name='null', email=postData['email'], password=bcrypt.hashpw(postData['pass1'].encode(), bcrypt.gensalt()))

    def login(self, postData):
        user_data = User.objects.filter(email=postData['email']).first()
        # print(user_obj)
        pwhash = user_data.password.encode()
        if pwhash == bcrypt.hashpw(postData['pass1'].encode(), pwhash):
            return True
        return False

    def set_session(self, postData):
        user_data = User.objects.filter(email=postData['email']).first()
        user_id = user_data.id
        return user_id

    def get_user_data_from_session(self, session_id):
        user_data = User.objects.filter(id=session_id).first()
        print(user_data)
        return user_data



class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=55)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
