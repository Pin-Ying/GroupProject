import pandas as pd
import re

'''
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
'''

def movieSearch(df,searchDic,screens=["Imax", "3D", "數位"]):

    ### 搜尋欄無填寫視為全搜尋
    if len(searchDic) == 1:
        return df.to_dict("records")
    
    ### 針對螢幕篩選先重新建構字典
    searchDic["movieScreen"] = []
    for screen in screens:
        if screen in searchDic.keys():
            searchDic["movieScreen"].append(screen)
            searchDic.pop(screen)
    if len(searchDic["movieScreen"])==0:
        searchDic.pop("movieScreen")

    try:
        ### 電影標題搜尋
        if "movieTitle" in searchDic:
            pattern = f"{searchDic['movieTitle']}"
            df["movieTitle"] = df["movieTitle"].map(
                lambda x: x if re.search(pattern, x) else None
            )
            df = df.dropna(subset=['movieTitle'])
        
        ### 電影螢幕搜尋
        if "movieScreen" in searchDic:
            df["movieScreen"] = df["movieScreen"].map(lambda x: x if x in searchDic["movieScreen"] else None)
            df = df.dropna(subset=["movieScreen"])
    
        datas = df.to_dict("records")

    except Exception as e:
        datas = [f"error!\n{e}"]
    return datas

if __name__=='__main__':
    df=pd.read_csv("movie.csv")
    df = df.rename(columns={'電影名稱': 'movieTitle','電影海報網址':'trailerLink','電影時長':'runningTime','電影螢幕':"movieScreen"})
    # searchDic={'csrfmiddlewaretoken':'模擬網頁回傳的csrf_token','movieTitle':'小丑：雙重瘋狂'}
    # searchDic={'csrfmiddlewaretoken':'模擬網頁回傳的csrf_token','數位':'on'}
    # searchDic={'csrfmiddlewaretoken':'模擬網頁回傳的csrf_token','movieTitle':'小丑','數位':'on'}
    searchDic={'csrfmiddlewaretoken':'模擬網頁回傳的csrf_token'}
    print(len(movieSearch(df,searchDic)))
    print(len(df))




