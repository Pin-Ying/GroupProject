from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models

# from django.http import HttpResponse


def user_logout(request):
    logout(request)
    return redirect("search_index")


def user_profile(request):
    return render(request, "user/profile.html")


def user_login(request):
    msg = ""
    user = None
    username = request.session.get("username", "")
    if request.method == "POST":
        if request.POST.get("login"):
            username = request.POST.get("username")
            password = request.POST.get("password")

            if username == "" or password == "":
                msg = "帳號密碼不能為空"
            else:
                user = authenticate(request, username=username, password=password)
                if user:
                    msg = "登入成功"
                    login(request, user)
                    return redirect("search_index")
                else:
                    msg = "帳號或密碼錯誤"

    return render(
        request, "user/login.html", {"msg": msg, "user": user, "username": username}
    )


def user_register(request):
    form = UserCreationForm()
    msg = ""

    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 密碼長度至少8
        if len(password1) < 8:
            msg = "密碼長度不正確"

        # 密碼相同
        elif password1 != password2:
            msg = "兩次密碼不相同"

        else:
            # 帳號是否存在
            if User.objects.filter(username=username):
                msg = "帳號已存在"

            # 註冊使用者
            else:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                msg = "註冊成功"
                request.session["username"] = user.username
                return redirect("search_index")

    return render(request, "user/register.html", {"form": form, "msg": msg})


# def a4(request):
#     genres = Movie.objects.values_list('genre', flat=True).distinct()
#     return render(request,'4.html',{"genres":genres})
