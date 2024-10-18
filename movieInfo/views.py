from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models.functions import Length
from django.http import HttpResponse
import random
import pandas as pd
from dataCrawl.models import movie, showTimeInfo, theater, Review
from dataCrawl.comments import import_reviews

# Create your views here.
def theaterInfo(request):
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

    return render(request,"theaterInfo/theaterInfo.html",{'cinema_groups': cinema_group_list,"tra":tra,"sj":sj,"url":url,"title":title})


def movieInfo(request, movieID):
    # import_reviews_from_csv()
    movie_data = movie.objects.get(id=movieID)
    show_data = showTimeInfo.objects.filter(movie=movieID)
    theater_data = theater.objects.all()
    movie_data = model_to_dict(movie_data)
    show_data = [model_to_dict(data) for data in show_data]
    for data in show_data:
        data["theater"] = theater_data.get(id=data["theater"])
    print(movie_data, show_data)

    # 查詢評論資料
    comments = Review.objects.filter(movie=movieID).values_list("content", flat=True)

    # 隨機選擇評論
    if not comments:
        random_comment = ["暫無評論"]
    elif len(comments) >= 3:
        random_comment = random.sample(list(comments), 3)  # 隨機選擇 3 條評論
    else:
        random_comment = list(comments)
    # context=None
    sorted_comments = comments.annotate(content_length=Length("content")).order_by(
        "-content_length"
    )
    # thread1 = threading.Thread(target=query_location)
    # thread1.start()

    return render(
        request,
        "movieInfo/movieInfo.html",
        {
            "movie": movie_data,
            "showInfo": show_data,
            "random_comment": random_comment,
            "movie_Comment": list(sorted_comments),
        },
    )

def submit_comment(request):
    if request.method == "POST":
        movie_name = request.POST.get("movie-name")
        comment = request.POST.get("comment")
        movie_data = movie.objects.get(title=movie_name)
        print(movie_name, movie_data)
        # 創建並保存評論
        review = Review(movie=movie_data, content=comment)
        review.save()
        return render(
            request,
            "comment_success.html",
            {"movie_name": movie_name, "movie_id": movie_data.id},
        )  # 成功頁面
