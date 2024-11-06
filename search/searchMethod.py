from dataCrawl.models import theater,showTimeInfo
from django.forms.models import model_to_dict
import pandas as pd
from datetime import datetime
import re

"""
紀錄各項目名稱如下:
搜尋項目(db_model) => html_name

電影名稱(movie.title) => movieTitle
電影螢幕(movie.screen_type) => movieScreen
    因為是用checkbox所以每個螢幕項目在html中都有name
    Imax => "Imax"
    3D => "3D"
    數位 => "數位"

欲觀看地區 => area
上映劇院(theater.name) => theater

最終以 datas 回傳給 html
"""

today=datetime.now().date()
today=today.strftime("%Y-%m-%d")
now=datetime.now().time()


def movieSearch(df, searchDic, screens=["Imax", "3D"]):

    ### 針對螢幕篩選先重新建構字典
    searchDic["movieScreen"] = []
    for screen in screens:
        if screen in searchDic.values():
            searchDic["movieScreen"].append(screen)
            searchDic.pop(screen)
    if len(searchDic["movieScreen"]) == 0:
        searchDic.pop("movieScreen")

    ### 搜尋欄無填寫視為全搜尋
    if len(searchDic) == 1:
        return df.to_dict("records"), searchDic

    try:
        ### 電影標題搜尋
        if "movieTitle" in searchDic:
            pattern = f"{searchDic['movieTitle']}"
            df["title"] = df["title"].map(
                lambda x: x if re.search(pattern, x) else None
            )
            df = df.dropna(subset=["title"])

        ### 電影螢幕搜尋
        if "movieScreen" in searchDic:
            for movieScreen in searchDic["movieScreen"]:
                
                df["screen_type"] = df["screen_type"].map(
                    lambda x: "Target" if movieScreen.upper() in x else x
                )
            df = df[df["screen_type"]=="Target"]

        datas = df.to_dict("records")
    except Exception as e:
        datas = [f"error!\n{e}"]
    return datas, searchDic


"""
北部區域：包括臺北市、新北市、基隆市、新竹市、桃園市、新竹縣及宜蘭縣。
中部區域：包括臺中市、苗栗縣、彰化縣、南投縣及雲林縣。
南部區域：包括高雄市、臺南市、嘉義市、嘉義縣、屏東縣及澎湖縣。
東部區域：包括花蓮縣及臺東縣。
福建省：包括金門縣與連江縣。
"""
northArea = [
    "臺北市",
    "台北市",
    "新北市",
    "基隆市",
    "新竹市",
    "桃園市",
    "新竹縣",
    "宜蘭縣",
]
centralArea = ["臺中市", "苗栗縣", "彰化縣", "南投縣", "雲林縣"]
southArea = ["高雄市", "臺南市", "嘉義市", "屏東縣", "澎湖縣"]
eastArea = ["花蓮縣", "臺東縣"]
islandsArea = ["金門縣", "連江縣"]

# '北部','中部','南部'
# 'north','central','south'
areas = {
    "north": northArea,
    "central": centralArea,
    "south": southArea,
    "east": eastArea,
    "islands": islandsArea,
}
cinema = ["威秀", "國賓", "美麗華", "秀太"]


### 篩選影城，包括日期
def theaterSearch(datas, searchDic):

    # 影城資料
    theater_datas = theater.objects.all()
    movieloc=pd.DataFrame([
                model_to_dict(theater)
                for theater in theater_datas
            ])

    # 影城與電影連結資料
    show_datas = showTimeInfo.objects.all()
    movietisr=pd.DataFrame([
                model_to_dict(show)
                for show in show_datas
            ])

    # 影院名稱篩影院 movieloc
    if "cinema" in searchDic:
        movieloc["cinema"] = movieloc["cinema"].map(
            lambda x: x if searchDic["cinema"] in x else None
        )
        movieloc = movieloc.dropna(subset=["cinema"])

    # 地區篩影院 movieloc
    movieloc["areaCheck"] = movieloc["address"].map(lambda x: x[:3])
    if "area" in searchDic:
        for county in areas[searchDic["area"]]:
            movieloc["areaCheck"] = movieloc["areaCheck"].map(
                lambda x: "Target" if county == x else x
            )
        movieloc = movieloc[movieloc["areaCheck"] == "Target"]

    # 電影 datas 對到影院名單 movietis(由 movieloc 篩選過)
    movietisr["theater"] = movietisr["theater"].map(
        lambda x: theater_datas.get(id=x).name if x in list(movieloc["id"]) else None
    )
    movietisr = movietisr.dropna(subset=["theater"])

    # 篩出特定日期、時間(如果日期為當日)的電影
    if "date" in searchDic:
        movietisr["date"]=movietisr["date"].map(
        lambda x: x if str(x)==searchDic['date'] else None
    )
        movietisr = movietisr.dropna(subset=["date"])
        if searchDic['date']==today:
            movietisr["time"]=movietisr["time"].map(
            lambda x: x if datetime.strptime(x, "%H:%M").time()>now else None
        )
            movietisr = movietisr.dropna(subset=["time"])

    results = []
    for data in datas:
        movieSet = set(movietisr["movie"])
        if data["id"] in movieSet:
            cinemas = movietisr[movietisr["movie"] == data["id"]][
                ["theater", "date", "time", "site"]
            ]
            data["theaters"] = list(set(cinemas["theater"]))
            cinemas = cinemas.to_dict("records")
            data["cinema"] = cinemas
            results.append(data)
    # print(results)

    return results



if __name__ == "__main__":
    print(now)
    # searchDic = {
    #     "csrfmiddlewaretoken": "7BIruF9y3jyO8ZYGEJG44mcrehZROhif1N9Xij04WRpclO2F0wL6vVU1Yu3hwfcq",
    #     "movieTitle": "小丑",
    #     "數位": "on",
    #     "area": "north",
    #     "cinema": "國賓",
    # }
    # searchDic = {
    #     "csrfmiddlewaretoken": "7BIruF9y3jyO8ZYGEJG44mcrehZROhif1N9Xij04WRpclO2F0wL6vVU1Yu3hwfcq"
    # }
    # searchDic={'csrfmiddlewaretoken': 'pPxS6lRVtGmm02JZex09jKZ81hxIcNZgj1YoUZIrmedKdRNYAk5bKjHILuB8ULTr', 'cinema': '威秀'}
