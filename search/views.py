from django.shortcuts import render
from search.models import movie
from search.searchMethod import movieSearch,theaterSearch
import pandas as pd

# test 123456789
# Create your views here.

def searchRequest(request, methods=["GET", "POST"], templatePage="searchPage.html"):
    if request.method == "GET":
        return render(request, templatePage)

    search = request.POST
    searchDic = {key: search[key] for key in search if search[key] != ""}
    print(searchDic)
    try:
        ### csv測試資料
        df=pd.read_csv("movie_csv/movie.csv")
        df = df.rename(columns={'電影名稱': 'movieTitle','電影海報網址':'trailerLink','電影時長':'runningTime','電影螢幕':"movieScreen"})
        
        ### 資料庫讀取全部資料
        # 從電影資料查詢(電影標題、選擇螢幕)
        movie_datas = movie.objects.all()
        movie_df = pd.DataFrame([{
            'movieTitle':movie.title,
            'movieScreen':movie.screen_type
        } for movie in movie_datas])
        
        # datas = movieSearch(df=movie_df,searchDic=searchDic)
        datas,searchDic = movieSearch(df=df,searchDic=searchDic)
        datas = theaterSearch(datas,searchDic)
        print(searchDic)
        # 從影院資料查詢(地區、影院)
        ### 製作中


    except Exception as e:
        print(e)
        datas = ["error!"]
        movie_datas = ["error!"]
    # return render(request, templatePage,{'datas':datas})
    return render(request, templatePage,{'movies':datas,'searchDic':searchDic})

