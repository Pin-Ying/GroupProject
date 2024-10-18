from django.shortcuts import render
from django.forms.models import model_to_dict
from dataCrawl.models import movie, showTimeInfo, theater
from search.searchMethod import movieSearch, theaterSearch
import pandas as pd
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

    return render(request, "ordering.html", {'context':context})
