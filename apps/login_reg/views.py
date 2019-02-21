from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
from datetime import datetime

def index(request):
    if 'user' in request.session:
        return redirect(success)
    return render(request, 'login_registration/index.html')

def register(request):

    if 'user' in request.session:
        return redirect(success)
    
    errors = User.objects.basic_validator(request.POST)

    context = {
        "first_name": request.POST['first_name'],
        "last_name": request.POST['last_name'],
        "email": request.POST['email']
    }

    if len(errors) > 0:
        for tag, value in errors.items():
            messages.error(request, value, extra_tags=tag)
        
        return render(request, 'login_registration/registration_page.html', context)
    else:
        
        #--- check if the email exist or not ---#
        user = User.objects.filter(email=request.POST['email'])
        if user:
            messages.error(request, "This email address already exist", extra_tags="email")
            return render(request, 'login_registration/registration_page.html', context)
        #--- check if the email exist or not ---#
        
        hashedPw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], hashpw=hashedPw)
        
        request.session['user'] = request.POST['first_name']
        request.session['user_id'] = user.id
        
        return redirect(success)

def get_login_page(request):
    if 'user' in request.session:
        return redirect(success)
    return render(request, 'login_registration/login_page.html')
    
def get_registration_page(request):
    if 'user' in request.session:
        return redirect(success)
    return render(request, 'login_registration/registration_page.html')

def login(request):

    if 'user' in request.session:
        return redirect(success)

    errors = User.objects.login_validator(request.POST)
    
    if len(errors) > 0:
        for tag, value in errors.items():
            messages.error(request, value, extra_tags=tag)
        return redirect(get_login_page)
    else:
        user = User.objects.filter(email=request.POST['lg_email'])
        for u in user:
            userdbpassword = u.hashpw
       
        if user and bcrypt.checkpw(request.POST['lg_password'].encode(), userdbpassword.encode()):
            request.session['user'] = user[0].first_name
            request.session['user_id'] = user[0].id
            return redirect(success)
        else:
            messages.error(request, "Invalid username or password", extra_tags='general')
            return redirect(get_login_page)

def success(request):
    if 'user' in request.session:
        return redirect('../book_review/book_index')
        # return render(request, 'login_registration/success.html')
    else:
        return redirect(index)

def logout(request):
    request.session.pop('user')
    request.session.pop('user_id')
    return redirect(index)
