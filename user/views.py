from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from dataCrawl.models import movie
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from dataCrawl.models import User,movie, theater,Click
from django.shortcuts import render
from django.forms.models import model_to_dict
from search.searchMethod import movieSearch, theaterSearch
from datetime import datetime,date
import pandas as pd
import re,random
from sklearn.metrics.pairwise import cosine_similarity

from django.contrib.auth import authenticate, login
from django.http import JsonResponse



today = date.today()
today_text = today.strftime("%m月%d日")

def logout(request):
    # logout(request)

    del request.session['username']
    del request.session['email']
    return redirect("search_index")


def user_profile(request):
    return render(request, "user/profile.html")


def user_login(request, templatePage="search/searchPage.html"):
    account_post = request.POST.get('account')
    password_post = request.POST.get('password')

    try:
        user = User.objects.get(account=account_post, password=password_post)
        # 如果找到用戶，檢查是否已經驗證過
        if user.verificationok:
            request.session['username'] = user.name  # 儲存使用者名稱到 session
            request.session['email'] = user.email
            request.session['msg'] ="登入成功!"
            return redirect("search_index")

        else:
            request.session['msg']="帳號未驗證，請先驗證!"
            return redirect("search_index")

    except User.DoesNotExist:
        # 如果沒有找到用戶
        request.session['msg']="帳號或密碼錯誤!"
        return redirect("search_index")

def user_register_new(request):
    movie_type = movie.objects.values_list('movie_type', flat=True).distinct()
    return render(request,'user/register_new.html',{"movie_type":movie_type})

def register(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        account=request.POST.get('account')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        email=request.POST.get('email')
        love=request.POST.get('love')
        movie_type = movie.objects.values_list('movie_type', flat=True).distinct()
        print(name,account,password,confirm_password,email,love)

        if not re.match(r'^[A-Za-z0-9]{6,}$', account):
            messages.error(request, '帳號必須至少包含 6 個字元，並且只能包含字母和數字')
            return render(request,'user/register_new.html',locals())

        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$', password):
            messages.error(request, 'password_post必須包含至少 8 個字元，且包括一個大寫字母、一個小寫字母和一個數字')
            return render(request,'user/register_new.html',locals())

        elif password != confirm_password:
            messages.error(request, '兩次輸入的password_post不一致')
            return render(request,'user/register_new.html',locals())
        
        elif User.objects.filter(account=account).exists():
            messages.error(request, '已有重複帳號')
            return render(request,'user/register_new.html',locals())

        # 檢查 Email 是否格式正確
        elif email:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, '請輸入正確的電子郵件格式')
                return render(request,'user/register_new.html',locals())

            if User.objects.filter(email=email).exists():
                messages.error(request, 'EMAIL已註冊')
                return render(request,'user/register_new.html',locals())


        randoms=random.randint(100000,999999)
        while User.objects.filter(verification_code=randoms).exists():
                randoms=random.randint(100000,999999)
        user = User()
        #寫入資料庫
        user.name = name  # 先不提交到資料庫
        user.account = account
        user.password = password  # 你可以在這裡進行加密
        user.email = email  # 隨機產生或發送驗證碼
        user.preferences = love  # 驗證狀態為未驗證
        user.verification_code=randoms
        user.save()  # 將資料保存到資料庫

        verification_link = request.build_absolute_uri(
            "http://127.0.0.1:8000/user/verificationok/" + f'?email={email}&verification_code={randoms}'
        )
        # https://nwepj-a8be4739b915.herokuapp.com/
        # http://127.0.0.1:8000/

        subject = '驗證你的帳號'
        message =  f'您好，{name}，您的驗證碼是：{randoms}\n\n點選此處驗證：{verification_link}'
        html_message = f"""
            <p>您好，{name}</p>
            <p>您的驗證碼是：{randoms}</p>
            <p>請點選以下連結進行驗證：</p>
            <a href="{verification_link}">點選此處驗證</a>
        """
        from_email = 'movie1131101@gmail.com'
        recipient_list = [email]
        send_mail(subject,message, from_email, recipient_list,html_message=html_message)

        return render(request,'user/logset.html',{"name":name})
    
def verificationok(request):
    ssss = request.GET.get("email")
    dddd = request.GET.get("verification_code")
    if ssss and dddd !=None:
        user = User.objects.get(email=ssss)
        print(user.verificationok)
        print(ssss,dddd)
        if not user.verificationok:
                # 如果 verificationok 為 True，檢查驗證碼是否匹配
                if user.verification_code == dddd:
                    user.verificationok = True
                    user.save()
                    # messages.success(request, '驗證成功！')
                    return render(request, 'user/restar.html')
    return render(request, 'user/restar.html')


def recommend(request):
    username = request.session.get('username')
    user = User.objects.get(name=username)
    user_id = user.id  # 假設目標使用者的ID

    # 取得點擊紀錄並轉換為 DataFrame
    clicks = Click.objects.all()
    data = [{'user': click.user.id, 'moviename': click.movie.title} for click in clicks]
    df = pd.DataFrame(data)

    # 建立點擊矩陣並計算相似度
    click_matrix = df.pivot_table(index='user', columns='moviename', aggfunc='size', fill_value=0)
    user_similarity = cosine_similarity(click_matrix)
    user_similarity_df = pd.DataFrame(user_similarity, index=click_matrix.index, columns=click_matrix.index)

    # 根據使用者相似度推薦電影
    recommended_movie = recommend_movies(user_id, click_matrix, user_similarity_df)
    
    if not request.session.get('recommended_movie'):
        request.session['recommended_movie'] = recommended_movie
    return redirect("search_index")

def recommend_movies(user_id, click_matrix, user_similarity_df, top_n=5):
    # 找到與目標使用者最相似的幾個使用者
    if user_id not in user_similarity_df.index:
        return ["沒有推薦的電影，因為使用者不在資料中"]

    # 找到與目標使用者最相似的幾個使用者
    similar_users = user_similarity_df.loc[user_id].sort_values(ascending=False).index[1:top_n+1]

    # 取得這些使用者點擊過的電影類型
    similar_users_clicks = click_matrix.loc[similar_users].sum()

    # 找出使用者點擊過的電影類型
    user_clicks = click_matrix.loc[user_id]

    # 將使用者的點擊次數與相似使用者的點擊次數合併
    combined_clicks = similar_users_clicks + user_clicks

    # 按照點擊次數排序，優先推薦點擊次數更多的類型
    recommendations = combined_clicks.sort_values(ascending=False)

    return recommendations.index.tolist()