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

'''
北部區域：包括臺北市、新北市、基隆市、新竹市、桃園市、新竹縣及宜蘭縣。
中部區域：包括臺中市、苗栗縣、彰化縣、南投縣及雲林縣。
南部區域：包括高雄市、臺南市、嘉義市、嘉義縣、屏東縣及澎湖縣。
東部區域：包括花蓮縣及臺東縣。
福建省：包括金門縣與連江縣。
'''
northArea=['臺北市','新北市','基隆市','新竹市','桃園市','新竹縣','宜蘭縣']
centralArea=['臺中市','苗栗縣','彰化縣','南投縣','雲林縣']
southArea=['高雄市','臺南市','嘉義市','屏東縣','澎湖縣']
eastArea=['花蓮縣','臺東縣']
islandsArea=['金門縣','連江縣']

# area=['北部','中部','南部']
area=['north','central','south']
cinema=["威秀","國賓","美麗華","秀太"]




### 預想：待功能完成，帶入movieSearch篩選的結果，在電影的datas出來時直接帶入datas
def theater_search(datas):
    movieloc=pd.read_csv('movie_csv/movieloc.csv')
    for data in datas:

        pass
    
    
if __name__=='__main__':
    df=pd.read_csv("movie_csv/movie.csv")
    df = df.rename(columns={'電影名稱': 'movieTitle','電影海報網址':'trailerLink','電影時長':'runningTime','電影螢幕':"movieScreen"})
    searchDic={'csrfmiddlewaretoken': '7BIruF9y3jyO8ZYGEJG44mcrehZROhif1N9Xij04WRpclO2F0wL6vVU1Yu3hwfcq', 'movieTitle': '小丑', '數位': 'on', 'area': 'north', 'cinema': '威秀'}
    data=movieSearch(df,searchDic)
    print(theater_search(data))

    


