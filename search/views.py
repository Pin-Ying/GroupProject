from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.db.models.functions import Length
from django.http import HttpResponse, JsonResponse
from search.models import movie, showTimeInfo, theater, Review
from search.searchMethod import movieSearch, theaterSearch
import pandas as pd
import time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from datetime import date

# test 123456789
# Create your views here.
today = date.today()
today_text = today.strftime("%m月%d日")


def searchRequest(
    request, methods=["GET", "POST"], templatePage="search/searchPage.html"
):
    searchDic = ""
    datas = ""

    try:
        ### 資料庫讀取全部資料
        # 從電影資料查詢(電影標題、選擇螢幕)
        movie_datas = movie.objects.all()
        df = pd.DataFrame([model_to_dict(movie) for movie in movie_datas])

        if request.method == "GET":
            searchDic = {"search": "all"}
            df = df.to_dict("records")
            datas = theaterSearch(df, searchDic) if len(df) > 0 else ""
            return render(request, templatePage, {"movies": datas})

        search = request.POST
        searchDic = {key: search[key] for key in search if search[key] != ""}

        # datas = movieSearch(df=movie_df,searchDic=searchDic)
        datas, searchDic = movieSearch(df=df, searchDic=searchDic)
        datas = theaterSearch(datas, searchDic)
        print(datas)

    except Exception as e:
        print(e)
    # return render(request, templatePage,{'datas':datas})
    return render(request, templatePage, {"movies": datas, "searchDic": searchDic})


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


# 清空評論資料表並導入新資料
def import_reviews_from_csv():
    # Review.objects.all().delete()  # 清空評論資料表

    # df = pd.read_csv('staticfiles/moviescom.csv', encoding='utf-8')  # 讀取 CSV 檔案
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    # url = "https://today.line.me/tw/v2/comment/movie/Kw8pGwr"
    # driver.get(url)
    time.sleep(5)  # Adjust the sleep time if necessary
    page_source = driver.page_source

    url = "https://today.line.me/tw/v2/movie/chart/trending"
    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source
    soups = BeautifulSoup(page_source, "html.parser")
    movieDict = {}

    href = []
    a1 = soups.find_all("a", "detailListItem-bookingButton")
    for i in a1:
        # print(i["href"])
        href.append("https://today.line.me" + i["href"])
    comment = {}
    for i in range(len(href)):
        co = []
        hre = href[i]
        driver.get(hre)
        time.sleep(5)
        page_source = driver.page_source
        soups = BeautifulSoup(page_source, "html.parser")
        name1 = soups.find("div", "filmLiteCard-title")
        comment[name1.text] = []
        a1 = soups.find_all("div", "commentItem-content")

        for i in a1:
            comment[name1.text].append(i.text)
    data = {"電影名稱": [], "評論": []}
    for i in comment:
        for j in comment[i]:
            data["電影名稱"].append(i)
            data["評論"].append(j)

    df = pd.DataFrame(data)
    for index, row in df.iterrows():
        try:
            movie_data = movie.objects.get(title=row["電影名稱"])
        except movie_data.DoesNotExist:
            print(f"電影 '{row['電影名稱']}' 在數據庫中不存在，跳過該排片。")
            continue  # 如果電影不存在，跳過當前行
        review, created = Review.objects.get_or_create(
            movie=movie_data, content=row["評論"]
        )


# 清空所有表並匯入新資料
def import_data(request):
    thread2 = import_reviews_from_csv()
    # import_reviews_from_csv()
    # import_movies()
    # import_reviews_from_csv()
    return HttpResponse("數據導入成功")


def seats(request):
    movie_title = request.GET.get("movie_title")
    theater_name = request.GET.get("theater")
    selected_room = ""
    selected_session = ""

    # 检查表单提交的影厅和场次信息
    if request.method == "POST":
        movie_title = request.POST.get("movie_title")
        theater_name = request.POST.get("theater")
        # selected_room = request.POST.get("room")
        # selected_session = request.POST.get("session")
    movie_data = movie.objects.get(title=movie_title)
    theater_data = theater.objects.get(name=theater_name)

    show_data = showTimeInfo.objects.filter(
        movie=movie_data,
        theater=theater_data,
        date=today,
    )
    room = []
    session = []
    for m in show_data:
        room.append(m.site)
        session.append(m.time)

    m_sessions = pd.DataFrame({"room": room, "session": session})
    print(m_sessions)

    session_data = m_sessions.to_dict(orient="records")

    context = {
        "current_date": today_text,
        "movie_poster_url": movie_data.img_src,  # 電影url
        "seat_map_url": theater_data,  # google map
        "session_data": session_data,  # 场次数据
        "theater_name": theater_data.name,
        "selected_room": selected_room,  # 当前选择的影厅
        "selected_session": selected_session,  # 当前选择的场次
    }
    print(movie_data.img_src)

    return render(request, "ordering.html", locals())
