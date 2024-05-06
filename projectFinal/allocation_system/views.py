from django.shortcuts import render, redirect, HttpResponse
from application.EmailBackEnd import EmailBackEnd
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from application.models import CustomUser


def BASE(request):
    return render(request, "base.html")

def LOGIN(request):
    return render(request, "login.html")

def doLogin(request):
    if request.method == "POST":
        user = EmailBackEnd.authenticate(
            request,
            username=request.POST.get("email"),
            password=request.POST.get("password"),
        )
        if user != None:
            login(request, user)
            user_type = user.user_type
            if user_type == "1":
                return redirect("admin_home")
            elif user_type == "2":
                return redirect('lecture_home')
            elif user_type == "3":
                return redirect('student_home')
            else:
                messages.error(request, "Email and Password Are Invalid!")
                return redirect("login")
        else:
            messages.error(request, "Email and Password Are Invalid!")
            return redirect("login")


def doLogout(request):
    logout(request)
    return redirect("login")


@login_required(login_url="/")
def PROFILE(request):
    try:
        user = CustomUser.objects.get(id=request.user.id)
        context = {
            "user": user,
        }
        return render(request, "profile.html", context)
    except:
        messages.error(request, 'User not found')
        render(request, '404_Not_Found.html')

@login_required(login_url="/")
def PROFILE_UPDATE(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            customuser.username = username

            if password != None and password != "":
                customuser.set_password(password)
            
            customuser.save()
            messages.success(request,'Your Profile Updated Successfully !')
            return redirect('profile')
        except:
            messages.error(request,'Failed To Update Your Profile')

    return render(request,'profile.html')

def error_404(request, exception):
    return render(request, '404_Not_Found.html')