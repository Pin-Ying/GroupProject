from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models.functions import Length
from django.http import HttpResponse
import random
from dataCrawl.models import movie, showTimeInfo, theater, Review
from dataCrawl.commits import import_reviews

# Create your views here.
def movieInfo(request, movieID):
    # import_reviews_from_csv()
    movie_data = movie.objects.get(id=movieID)
    movie_id = movie_data.id
    show_data = showTimeInfo.objects.filter(movie=movieID)
    theater_data = theater.objects.all()
    movie_data = model_to_dict(movie_data)
    show_data = [model_to_dict(data) for data in show_data]
    for data in show_data:
        data["theater"] = theater_data.get(id=data["theater"])
    print(movie_data, show_data)

    # 查詢評論資料
    comments = Review.objects.filter(movie=movie_id).values_list("content", flat=True)

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
        "movieInfo.html",
        {
            "movie": movie_data,
            "showInfo": show_data,
            "random_comment": random_comment,
            "movie_Comment": list(sorted_comments),
        },
    )

def submit_comment(request):
    if request.method == "POST":
        movie_name = request.POST.get("電影名稱")
        comment = request.POST.get("comment")
        movie_data = movie.objects.filter(title=movie_name).first()
        print(movie_name, movie_data)
        # 創建並保存評論
        review = Review(movie=movie_data, content=comment)
        review.save()
        return render(
            request,
            "comment_success.html",
            {"movie_name": movie_name, "movie_id": movie_data.id},
        )  # 成功頁面


# 清空所有表並匯入新資料
def import_data(request):
    thread2 = import_reviews()
    # import_reviews_from_csv()
    # import_movies()
    # import_reviews_from_csv()
    return HttpResponse("數據導入成功")