from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models.functions import Length
from django.http import HttpResponse
from django.utils import timezone
import random
import pandas as pd
from dataCrawl.models import movie, showTimeInfo, theater
from user.models import Review, Click, User
from user.models import Movie as user_movie
from dataCrawl.comments import import_reviews
from datetime import datetime

now=datetime.now()
now=timezone.make_aware(now)

# Create your views here.
def theaterInfo(request):
    username=request.session['username'] if 'username' in request.session else None
    data=pd.read_csv("staticfiles/csv/theaterInfo.csv",encoding="utf-8")

    cinema_groups = {}
        # 遍歷數據的每一行
    for index, row in data.iterrows():
        group_name = row['影城']  # 影城名稱
        cinema_name = row['戲院']  # 戲院名稱

        # 如果影城名稱不在字典中，則初始化
        if group_name not in cinema_groups:
            cinema_groups[group_name] = []

        # 將戲院名稱加入到相應的影城下
        cinema_groups[group_name].append(cinema_name)

    # 將字典轉換為列表格式
    cinema_group_list = [{'group_name': group_name, 'cinemas': cinemas} for group_name, cinemas in cinema_groups.items()]
    if request.method=='GET': 
        cinema=request.GET['theaterID']
        cinema=theater.objects.get(id=cinema).name
    else:
        cinema=request.POST['cinema_select']
    selected_row = data[data['戲院'] == cinema]
    tra = selected_row['交通方式'].iloc[0]
    sj=selected_row['介紹'].iloc[0]
    url=selected_row['戲院海報'].iloc[0]
    title=selected_row['戲院'].iloc[0]

    return render(request,"theaterInfo/theaterInfo.html",{'cinema_groups': cinema_group_list,"tra":tra,"sj":sj,"url":url,"theater_title":title,"username":username})


def movieInfo(request, movieID):
    username = None
    if 'username' in request.session:
        username = request.session['username']
        user = User.objects.get(name=username)
        user_id = user.id
        # 查詢點擊的電影類型
        movie_title = movie.objects.get(id=movieID).title
        Click.objects.create(user_id=user_id, movie_title=movie_title,clicked_at=datetime.now())
        print(username)
    # import_reviews_from_csv()
    movie_data = movie.objects.get(id=movieID)
    youtube_url = movie_data.trailer_link or ""
    user_movie_data=user_movie.objects.get(title=movie_data.title)
    show_data = showTimeInfo.objects.filter(movie=movieID)
    theater_data = theater.objects.all()
    movie_data = model_to_dict(movie_data)
    show_data = [model_to_dict(data) for data in show_data]
    for data in show_data:
        data["theater"] = theater_data.get(id=data["theater"])
    print(movie_data, show_data)

    # 查詢評論資料
    comments = Review.objects.filter(movie=user_movie_data).values_list("content", flat=True)

    # 隨機選擇評論
    if not comments:
        random_comment = ["暫無評論"]
    elif len(comments) >= 3:
        random_comment = random.sample(list(comments), 3)  # 隨機選擇 3 條評論
    else:
        random_comment = list(comments)
    sorted_comments = comments.annotate(content_length=Length("content")).order_by(
        "-content_length"
    )

    return render(
        request,
        "movieInfo/movieInfo.html",
        {
            "movie": movie_data,
            "showInfo": show_data,
            "random_comment": random_comment,
            "movie_Comment": list(sorted_comments),
            'username':username,
            "youtube_url":youtube_url,
            
        },
    )

def submit_comment(request):
    username=request.session['username'] if 'username' in request.session else None
    if request.method == "POST" and username:
        user = User.objects.get(name=username)
        movie_name = request.POST.get("movie-name")
        comment = request.POST.get("comment")
        movie_data = user_movie.objects.get(title=movie_name)
        movie_id=movie.objects.get(title=movie_name).id
        print(movie_name, movie_data)
        # 創建並保存評論
        review = Review(user=user,movie=movie_data, content=comment)
        review.save()
        return render(
            request,
            "comment_success.html",
            {"movie_name": movie_name, "movie_id": movie_id,"username":username},
        )  # 成功頁面
    return HttpResponse('登入後才能留言')
