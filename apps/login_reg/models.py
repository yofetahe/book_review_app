from django.db import models

# Create your models here.
from django.db import models
import re

class UsersManager(models.Manager):

    def basic_validator(self, postData):

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        NAME_REGEX = re.compile(r'^[a-zA-Z ]')
        PASSWORD_1_REGEX = re.compile(r'^[A-Z]')
        PASSWORD_2_REGEX = re.compile(r'^[0-9]')

        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be filled or should be longer than 2 character"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors['first_name'] = "First name must contain only character"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be filled or should be longer than 2 character"
        else:
            if not NAME_REGEX.match(postData['last_name']):
                errors['last_name'] = "Last name must contain only character"
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Please enter valid email address"
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        if len(postData['confirmpw']) == 0:
            errors['confirmpw'] = "Password is required"
        if (len(postData['confirmpw']) > 0 and len(postData['password']) > 0) and postData['password'] != postData['confirmpw']:
            errors['password'] = "Password doesn't match"
        
        return errors
    
    def login_validator(self, postData):
        errors = {}
        if len(postData['lg_email']) == 0 or len(postData['lg_password']) == 0:
            errors['general'] = "Email and password are required to login to the app"
                
        return errors

    def user_info_validator(self, postData):
        
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
        NAME_REGEX = re.compile(r'^[a-zA-Z ]')

        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be filled or should be longer than 2 character"
        else:
            if not NAME_REGEX.match(postData['first_name']):
                errors['first_name'] = "First name must contain only character"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be filled or should be longer than 2 character"
        else:
            if not NAME_REGEX.match(postData['last_name']):
                errors['last_name'] = "Last name must contain only character"
        if len(postData['email']) == 0:
            errors['email'] = "Email is required"
        else:
            if not EMAIL_REGEX.match(postData['email']):
                errors['email'] = "Please enter valid email address"
        return errors

    def user_password_validator(self, postData):
        errors = {}
        if len(postData['password']) == 0:
            errors['password'] = "Password is required"
        if len(postData['confirmpw']) == 0:
            errors['confirmpw'] = "Password is required"
        if (len(postData['confirmpw']) > 0 and len(postData['password']) > 0) and postData['password'] != postData['confirmpw']:
            errors['password'] = "Password doesn't match"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)
    email = models.EmailField(max_length=225)
    hashpw = models.CharField(max_length=255)
    description = models.TextField(null=True)
    user_level = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()