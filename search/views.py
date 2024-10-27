from django.shortcuts import render
from django.forms.models import model_to_dict
from django.db.models import Max
from django.utils import timezone
from dataCrawl.models import movie, showTimeInfo, theater
from search.searchMethod import movieSearch, theaterSearch
from datetime import datetime,timedelta
import pandas as pd
import json

# test 123456789
# Create your views here.
today = datetime.today()
today=timezone.make_aware(today)
today_text = today.strftime("%m月%d日")
dayStart=today.strftime("%Y-%m-%d")
# dayEnd=today + timedelta(days=7)
dayEnd=showTimeInfo.objects.aggregate(Max('date'))['date__max']
dayEnd=dayEnd.strftime("%Y-%m-%d") if dayEnd else today + timedelta(days=7)


def test(request):
    return render(request, "index_test.html")


def searchRequest(
    request, methods=["GET", "POST"], templatePage="search/searchPage.html"
):
    msg=""
    searchDic = ""
    datas = ""
    cinema_datas = ""
    if 'msg' in request.session:
        msg=request.session['msg']
        del request.session['msg']

    username=request.session['username'] if 'username' in request.session else None

    try:
        ### 資料庫讀取全部資料
        # 從電影資料查詢(電影標題、選擇螢幕)
        movie_datas = movie.objects.all()
        if 'recommended_movie' in request.session:
            recommended_movie=request.session['recommended_movie']
            del request.session['recommended_movie']
            movie_datas = movie.objects.filter(title__in=recommended_movie)
        cinema_datas = list(theater.objects.values_list("cinema", flat=True).distinct())
        print(cinema_datas)
        df = pd.DataFrame([model_to_dict(movie) for movie in movie_datas])

        if request.method == "GET":
            searchDic = {"search": "all"}
            df = df.to_dict("records")
            datas = theaterSearch(df, searchDic) if len(df) > 0 else ""
            return render(
                request, templatePage, {"movies": datas, "cinemas": cinema_datas,"dayStart": dayStart,
            "dayEnd":dayEnd,'select_day':dayStart,"msg":msg,"username":username}
            )

        search = request.POST
        searchDic = {key: search[key] for key in search if search[key] != ""}

        # datas = movieSearch(df=movie_df,searchDic=searchDic)
        datas, searchDic = movieSearch(df=df, searchDic=searchDic)
        datas = theaterSearch(datas, searchDic)
        print(datas)

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
            "dayEnd":dayEnd,
            'select_day':searchDic['date'] if 'date' in searchDic else dayStart,
            "msg":msg,
            "username":username
        },
    )


def theaters(request):
    username=request.session['username'] if 'username' in request.session else None
    theaters = theater.objects.all()
    cinema_list = list(set(theater.cinema for theater in theaters))
    return render(
        request,
        "search/theaterPage.html",
        {"theaters": theaters, "cinemas": cinema_list, 'username':username},
    )

def seats(request):
    username=request.session['username'] if 'username' in request.session else None
    selected_room = ""
    selected_session = ""
    movie_title=""
    theater_name=""

    if request.method == "GET":
        request.session['movie_title'] = movie_title = request.GET["movie_title"]
        request.session['theater_name'] = theater_name = request.GET["theater"]
        select_day= request.GET["select_day"]
        select_day=datetime.strptime(select_day, '%Y-%m-%d').date()
    
    ### 日期變動
    if request.method=='POST':
        data = json.loads(request.body)
        select_day = data.get("select_day")
        select_day=datetime.strptime(select_day, '%Y年%m月%d日').date()
        print('select_day:',select_day)

        movie_title=request.session['movie_title']
        theater_name=request.session['theater_name']
        # selected_room = request.POST.get("room")
        # selected_session = request.POST.get("session")
    movie_data = movie.objects.get(title=movie_title)
    theater_data = theater.objects.get(name=theater_name)
    dates=showTimeInfo.objects.filter(movie=movie_data,theater=theater_data).values_list('date',flat=True).distinct()
    show_data = showTimeInfo.objects.filter(movie=movie_data,theater=theater_data,date=select_day)

    room = []
    session = []
    for m in show_data:
        room.append(m.site)
        session.append(m.time)

    m_sessions = pd.DataFrame({"room": room, "session": session})

    session_data = m_sessions.to_dict(orient="records")

    context = {
        "theater": theater_data,
        "dates": dates,
        "current_date": select_day,
        "movie_poster_url": movie_data.img_src,
        "seat_map_url": theater_data,
        "session_data": session_data,
        "theater_title": theater_data.name,
        "selected_room": selected_room,
        "selected_session": selected_session,
        'username':username
    }

    return render(request, "search/ordering.html", context)
