from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from django.http import HttpResponse,JsonResponse
from search.models import movie,showTimeInfo,theater
from search.searchMethod import movieSearch, theaterSearch
import pandas as pd

# test 123456789
# Create your views here.

def searchRequest(request, methods=["GET", "POST"], templatePage="search/searchPage.html"):
    searchDic=""
    datas=""
        
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
            datas=theaterSearch(df,searchDic) if len(df)>0 else ""
            return render(request, templatePage,{"movies": datas})

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

def movieInfo(request,movieID):
    movie_data = movie.objects.get(id=movieID)
    show_data=showTimeInfo.objects.filter(movie=movieID)
    theater_data=theater.objects.all()
    movie_data=model_to_dict(movie_data)
    show_data=[model_to_dict(data) for data in show_data]
    for data in show_data:
        data["theater"]=theater_data.get(id=data["theater"])
    print(movie_data,show_data)
    return render(request,"moviePage.html",{"movie":movie_data,"showInfo":show_data})



