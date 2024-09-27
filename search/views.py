from django.shortcuts import render
from search.models import movie
import re
import pandas as pd

# test 123456789
# Create your views here.


def search(request, methods=["GET", "POST"]):
    if request.method == "GET":
        return render(request, "search.html")

    search = request.POST
    searchDic = {key: search[key] for key in search if search[key] != ""}

    ### 資料庫讀取全部資料
    datas = movie.objects.all()
    datas = [
        {
            "movieTitle": data.title,
            "movieScreen": data.screen,
        }
        for data in datas
    ]
    ### DataFrame
    df = pd.DataFrame(datas)

    ### 搜尋欄無填寫視為全搜尋
    if len(searchDic) == 1:
        results = datas
        return render(request, "search.html", locals())

    ### 針對螢幕篩選先重新建構字典
    screens = ["Imax", "3D", "digital"]
    searchDic["movieScreen"] = []
    for screen in screens:
        if screen in searchDic.keys():
            searchDic["movieScreen"].append(screen)
            searchDic.pop(screen)
    print(searchDic)

    try:
        ### 電影標題搜尋
        if "movieTitle" in searchDic:
            pattern = f"{searchDic['movieTitle']}"
            df["movieTitle"] = df["movieTitle"].map(
                lambda x: x if re.search(pattern, x) else None
            )
            df = df.dropna()

        ### DataFrame
        for key in ["movieScreen", "theater"]:
            if key in searchDic and len(searchDic[key]) != 0:
                df[key] = df[key].map(lambda x: x if x in searchDic[key] else None)
        datas = df.dropna()
        datas = datas.to_dict("records")
        print(datas)

    except Exception as e:
        print(e)
        datas = ["error!"]

    return render(request, "search.html", locals())
