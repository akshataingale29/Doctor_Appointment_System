from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.contrib import messages
from members.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout



def home(request):
    return render(request, "index.html")

def signup(request):
    print("Signup view called")
    print(f"Request method: {request.method}")
    print(f"POST data: {request.POST}")
    
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    else:
        if request.method == "POST": # To register users.
            try:
                fname = request.POST.get('fname')
                lname = request.POST.get('lname')
                city = request.POST.get('city')
                mob = request.POST.get('mob')
                email = request.POST.get('email')
                cemail = request.POST.get('cemail')
                passwd = request.POST.get('passwd')
                cpasswd = request.POST.get('cpasswd')

                # Debug information
                print(f"Form data: {fname}, {lname}, {email}, {cemail}, {mob}, {city}")

                if email != cemail:
                    mstr1 = 'Email and Confirm Email are not same.'
                    messages.error(request, mstr1)
                    return HttpResponseRedirect('/signup/')
                if passwd != cpasswd:
                    mstr2 = 'Password and Confirm Password are not same.'
                    messages.error(request, mstr2)
                    return HttpResponseRedirect('/signup/')

                # Check if user already exists
                if User.objects.filter(email=cemail).exists():
                    messages.error(request, 'A user with that email already exists.')
                    return HttpResponseRedirect('/signup/')

                user = User.objects.create_user(email=cemail, password=cpasswd)
                user.first_name = fname
                user.last_name = lname
                user.mobile = mob
                user.city = city
                user.save()
                
                print(f"User created: {user.email}")
                
                mstr3 = 'Your account has been successfully created.'
                messages.success(request, mstr3)
                return HttpResponseRedirect("/login/")

            except Exception as e:
                print(f"Error in signup: {str(e)}")
                messages.error(request, f"Error creating account: {str(e)}")
                return HttpResponseRedirect('/signup/')
        
        return render(request, "signup.html")

def login(request):
    print("Login view called")
    print(f"Request method: {request.method}")
    print(f"POST data: {request.POST}")
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')

def admin_login(request):
    print("Admin Login view called")
    print(f"Request method: {request.method}")
    print(f"POST data: {request.POST}")
    
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None and user.is_hospital_admin:
            auth_login(request, user)
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid admin credentials')
            return redirect('admin_login')
    
    return render(request, 'admin_login.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/')
    