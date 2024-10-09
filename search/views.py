from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from search.models import movie
from search.searchMethod import movieSearch, theaterSearch
import pandas as pd
from .dataCrawl import miramar
from . import dbUpdate
from django.http import HttpResponse
# test 123456789
# Create your views here.

def UpdateMovies(request):
    ### 美麗華
    df=miramar.get_movie()
    datas=df.to_dict("records")
    for data in datas:
        dbUpdate.movieUpdate(data)
    return HttpResponse('finish!')

def UpdateTheater(request):
    ### 美麗華
    df=miramar.get_theater()
    datas=df.to_dict("records")
    for data in datas:
        dbUpdate.theaterUpdate(data)
    return HttpResponse('finish!')

def UpdateShow(request):
    ### 美麗華
    df=miramar.get_showTimeInfo()
    datas=df.to_dict("records")
    for data in datas:
        dbUpdate.showUpdate(data)
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
