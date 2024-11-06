from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.forms.models import model_to_dict
from django.db.models import Max
from django.utils import timezone
from dataCrawl.models import movie, showTimeInfo, theater
from user.models import User
from search.searchMethod import movieSearch, theaterSearch
from datetime import datetime, timedelta
import pandas as pd
import json
from dataCrawl.datafrom.seatMap import findSeats

# test 123456789
# Create your views here.
today = datetime.today()
today = timezone.make_aware(today)
now=today.time()
now=timezone.make_aware(now)
today_text = today.strftime("%m月%d日")
dayStart = today.strftime("%Y-%m-%d")
# dayEnd=today + timedelta(days=7)
dayEnd = showTimeInfo.objects.aggregate(Max("date"))["date__max"]
dayEnd = dayEnd.strftime("%Y-%m-%d") if dayEnd else today + timedelta(days=7)


def test(request):
    return render(request, "index_test.html")


def searchRequest(
    request, methods=["GET", "POST"], templatePage="search/searchPage.html"
):
    msg = ""
    searchDic = ""
    datas = ""
    cinema_datas = ""
    username = None
    if "msg" in request.session:
        msg = request.session["msg"]
        del request.session["msg"]

    if "username" in request.session:
        username = request.session["username"]
        user = User.objects.get(name=username)
        preferences = user.preferences  # 取得使用者偏好
        preferences_list = preferences.split(",") if preferences else []

        # 根據偏好列表進行替換
        if "卡通動畫" in preferences_list:
            preferences_list = [
                "動畫" if p == "卡通動畫" else p for p in preferences_list
            ]
        elif "動畫" in preferences_list:
            preferences_list = ["動畫" if p == "動畫" else p for p in preferences_list]

    try:
        ### 資料庫讀取全部資料
        # 從電影資料查詢(電影標題、選擇螢幕)
        datas, upcoming_datas = "", ""
        movie_datas = movie.objects.filter(release_date__lte=today)
        if "recommended_movie" in request.session:
            recommended_movie = request.session["recommended_movie"]
            del request.session["recommended_movie"]
            movie_datas = movie_datas.filter(title__in=recommended_movie)

        upcoming_movies = movie.objects.filter(release_date__gt=today)
        cinema_datas = list(theater.objects.values_list("cinema", flat=True).distinct())
        print(cinema_datas)
        df = pd.DataFrame([model_to_dict(movie) for movie in movie_datas])
        df_upcoming = pd.DataFrame([model_to_dict(movie) for movie in upcoming_movies])

        df_upcoming = df_upcoming.to_dict("records")
        upcoming_datas = (
            theaterSearch(df_upcoming, {"search": "all"})
            if len(df_upcoming) > 0
            else ""
        )

        if request.method == "GET":
            searchDic = {"search": "all"}
            df = df.to_dict("records")
            datas = theaterSearch(df, searchDic) if len(df) > 0 else ""

            if preferences_list:
                datas = sorted(
                    datas,
                    key=lambda x: sum(
                        pref in x["movie_type"] for pref in preferences_list
                    ),
                    reverse=True,
                )
            return render(
                request,
                templatePage,
                {
                    "movies": datas,
                    "cinemas": cinema_datas,
                    "dayStart": dayStart,
                    "dayEnd": dayEnd,
                    "select_day": dayStart,
                    "msg": msg,
                    "username": username,
                    "upcoming_movies": upcoming_datas,
                },
            )

        search = request.POST
        searchDic = {key: search[key] for key in search if search[key] != ""}
        print(searchDic)

        # datas = movieSearch(df=movie_df,searchDic=searchDic)
        datas, searchDic = movieSearch(df=df, searchDic=searchDic)
        datas = theaterSearch(datas, searchDic)
        # print(datas)

    except Exception as e:
        print(e)
    # return render(request, templatePage,{'datas':datas})
    return render(
        request,
        templatePage,
        {
            "movies": datas,
            "cinemas": cinema_datas,
            "dayStart": dayStart,
            "dayEnd": dayEnd,
            "select_day": searchDic["date"] if "date" in searchDic else dayStart,
            "msg": msg,
            "username": username,
            "upcoming_movies": upcoming_datas,
        },
    )


def theaters(request):
    username = request.session["username"] if "username" in request.session else None
    theaters = theater.objects.all()
    cinema_list = list(set(theater.cinema for theater in theaters))
    return render(
        request,
        "search/theaterPage.html",
        {"theaters": theaters, "cinemas": cinema_list, "username": username},
    )


def seats(request):
    username = request.session["username"] if "username" in request.session else None
    selected_room = []
    selected_session = []
    movie_title = request.session["movie_title"] if "movie_title" in request.session else ""
    theater_name = request.session["theater_name"] if "theater_name" in request.session else ""
    select_day = request.session["select_day"] if "select_day" in request.session else ""
    seatImage = ""
    msg = ""

    try:
        if request.method == "GET":
            request.session["movie_title"] = movie_title = request.GET["movie_title"]
            request.session["theater_name"] = theater_name = request.GET["theater"]
            select_day = request.GET["select_day"]
            select_day = datetime.strptime(select_day, "%Y-%m-%d").date()
            request.session["select_day"] = select_day.strftime("%Y-%m-%d")

        if request.method == "POST":
            movie_title = request.session["movie_title"]
            theater_name = request.session["theater_name"]

            ### 日期變動
            if "select_day" in request.POST:
                select_day = request.POST["select_day"]
                print(select_day)
                select_day = datetime.strptime(select_day, "%Y年%m月%d日").date()
                request.session["select_day"] = select_day.strftime("%Y-%m-%d")
                print("select_day:", select_day.strftime("%Y-%m-%d"))

            elif "room" in request.POST and "session" in request.POST:
                selected_room = [request.POST.get("room")]
                selected_session = [request.POST.get("session")]
                select_day = request.session["select_day"]
                select_day = datetime.strptime(select_day, "%Y-%m-%d").date()
                emptySeat, bookedSeat, seatImage = findSeats(
                    theater_name,
                    movie_title,
                    select_day,
                    selected_room,
                    selected_session,
                )
                msg = "不好意思，該場次暫無座位資料" if emptySeat == "暫無資料" else msg

    except Exception as e:
        msg = "載入過程出現錯誤"
        print(str(e))

    movie_data = movie.objects.get(title=movie_title)
    theater_data = theater.objects.get(name=theater_name)
    dates = (
        showTimeInfo.objects.filter(movie=movie_data, theater=theater_data)
        .values_list("date", flat=True)
        .distinct()
    )
    show_data = showTimeInfo.objects.filter(
        movie=movie_data, theater=theater_data, date=select_day
    )

    print("日期：", select_day)  # debug
    print("戲院：", theater_name)  # debug
    print("電影：", movie_title)  # debug
    print("影廳：", selected_room)  # debug
    print("場次：", selected_session)  # debug

    m_sessions = [{"room": data.site, "session": data.time} for data in show_data]
    if select_day==today.date():
        m_sessions = [{"room": data.site, "session": data.time} for data in show_data if datetime.strptime(data.time,'%H:%S').time()>now]

    m_sessions = pd.DataFrame(m_sessions)

    session_data = m_sessions.to_dict(orient="records")

    context = {
        "theater": theater_data,
        "dates": dates,
        "current_date": select_day,
        "movie_poster_url": movie_data.img_src,
        "seat_map_url": seatImage,
        "session_data": session_data,
        "theater_title": theater_data.name,
        "selected_room": selected_room,
        "selected_session": selected_session,
        "username": username,
        "msg": msg,
    }

    return render(request, "search/ordering.html", context)


def home(request):
    return render(request, "home.html")
