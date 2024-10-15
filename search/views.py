from django.shortcuts import render,redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from search.models import movie,showTimeInfo,theater
from search.searchMethod import movieSearch, theaterSearch
import pandas as pd
import threading,json
from .dataCrawl import miramar,ambassador
from . import dbUpdate

from django.http import HttpResponse
# test 123456789
# Create your views here.

def UpdateMiramar(request):
    try:
        mir_movie=miramar.get_movie().to_dict("records")
        mir_show=miramar.get_showTimeInfo().to_dict("records")
        dbUpdate.movieUpdate(mir_movie)
        dbUpdate.showUpdate(mir_show)
        return JsonResponse({'status':'finish!'})
    except Exception as e:
        return JsonResponse({'status':'error!'+str(e)})



def UpdateMovies(request):
    ### datas
    ### 美麗華
    mir_movie=miramar.get_movie().to_dict("records")
    mir_show=miramar.get_showTimeInfo().to_dict("records")

    ### 國賓
    amb_movie,amb_show=[data.to_dict("records") for data in ambassador.get_movie_and_show()]

    dbUpdate.movieUpdate(mir_movie)
    dbUpdate.showUpdate(mir_show)
    dbUpdate.movieUpdate(amb_movie)
    dbUpdate.showUpdate(amb_show)

    # mir_threads
    # movieT=threading.Thread(dbUpdate.movieUpdate(mir_movie))
    # showT=threading.Thread(dbUpdate.showUpdate(mir_show))
    # movieT.start()
    # showT.start()
    # movieT.join()
    # showT.join()

    ### amb_threads
    # movieT=threading.Thread(dbUpdate.movieUpdate(amb_movie))
    # showT=threading.Thread(dbUpdate.showUpdate(amb_show))
    # movieT.start()
    # showT.start()
    # movieT.join()
    # showT.join()

    return JsonResponse({"result": "finish!"})

def UpdateTheater(request):
    ### 美麗華
    df=miramar.get_theater()
    datas=df.to_dict("records")
    dbUpdate.theaterUpdate(datas)
    
    ### 國賓
    df=ambassador.get_theater()
    datas=df.to_dict("records")
    dbUpdate.theaterUpdate(datas)

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
    return render(request,"search/searchTest.html")




