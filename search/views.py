from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from search.models import movie,showTimeInfo,theater
from search.searchMethod import movieSearch, theaterSearch
import pandas as pd
from .dataCrawl import miramar,ambassador
from . import dbUpdate
from django.http import HttpResponse
# test 123456789
# Create your views here.

def UpdateMovies(request):
    ### 美麗華
    # 電影
    df=miramar.get_movie()
    datas=df.to_dict("records")
    for data in datas:
        dbUpdate.movieUpdate(data)
    
    # 電影場次
    df=miramar.get_showTimeInfo()
    datas=df.to_dict("records")
    for data in datas:
        dbUpdate.showUpdate(data)
    
    ### 國賓
    df1,df2=ambassador.get_movie_and_show()
    datas=df1.to_dict("records")
    for data in datas:
        dbUpdate.movieUpdate(data)
    datas=df2.to_dict("records")
    for data in datas:
        dbUpdate.showUpdate(data)


    return HttpResponse('finish!')

def UpdateTheater(request):
    ### 美麗華
    df=miramar.get_theater()
    datas=df.to_dict("records")
    for data in datas:
        dbUpdate.theaterUpdate(data)
    
    ### 國賓
    df=ambassador.get_theater()
    datas=df.to_dict("records")
    for data in datas:
        dbUpdate.theaterUpdate(data)

    return HttpResponse('finish!')


def searchRequest(request, methods=["GET", "POST"], templatePage="search/searchPage.html"):
        
    try:
        ### 資料庫讀取全部資料
        # 從電影資料查詢(電影標題、選擇螢幕)
        movie_datas = movie.objects.all()
        df = pd.DataFrame(
            [
                model_to_dict(movie)
                for movie in movie_datas
            ]
        )
        screentypes=[]

        if request.method == "GET":
            searchDic={'search':'all'}
            df=df.to_dict("records")
            datas=theaterSearch(df,searchDic)
            return render(request, templatePage,{"movies": datas})

        search = request.POST
        searchDic = {key: search[key] for key in search if search[key] != ""}

        # datas = movieSearch(df=movie_df,searchDic=searchDic)
        datas, searchDic = movieSearch(df=df, searchDic=searchDic)
        datas = theaterSearch(datas, searchDic)
        print(datas)


    except Exception as e:
        print(e)
        datas = ["error!"]
        movie_datas = ["error!"]
    # return render(request, templatePage,{'datas':datas})
    return render(request, templatePage, {"movies": datas, "searchDic": searchDic})

def movieInfo(request,movieID):
    movie_data = movie.objects.get(id=movieID)
    show_data=showTimeInfo.objects.filter(movie=movieID)
    theater_data=theater.objects.all()
    movie_data=model_to_dict(movie_data)
    show_data=[model_to_dict(data) for data in show_data]
    for data in show_data:
        data["theater"]=theater_data[data["theater"]]
    print(movie_data,show_data)
    return render(request,"moviePage.html",{"movie":movie_data,"showInfo":show_data})

def test(request):
    ### 美麗華
    # 電影
    test1=miramar.get_movie()
    test1=test1.to_dict("records")
    
    # 電影場次
    test2=miramar.get_showTimeInfo()
    test2=test2.to_dict("records")

    ### 國賓
    test3,test4=ambassador.get_movie_and_show()
    test3,test4=test3.to_dict("records"),test4.to_dict("records")
    return render(request,"search/searchTest.html",locals())




