from bs4 import BeautifulSoup
import requests
import pandas as pd
from datetime import datetime

def get_soup(url):
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

totle=[]
moviename,movieposterurl,movieupday,moviescreen = [],[],[],[]
urls1,urls2,Previewurl=[],[],[]
cast,movetype,times,movsj=[],[],[],[]


def get_movie():
    soup=get_soup("https://www.miramarcinemas.tw/Movie/Index?type=now") #上映
    for movie_item in soup.find_all('li', class_='col s6 m4 l3'):
        # 取得電影名稱
        movie_name = movie_item.find('div', class_='title').contents[0].strip() 
        moviename.append(movie_name)
        # 取得電影海報網址
        poster_url = movie_item.find('a', class_='img').find('img')['src']
        movieposterurl.append(poster_url)
        # 取得上映日期
        release_date = movie_item.find('span', class_='date').get_text(strip=True)
        movieupday.append(release_date)
        # 取得畫面格式
        screen_formats = ', '.join([badge.get_text(strip=True) for badge in movie_item.find('div', class_='badge_area').find_all('a')])
        moviescreen.append(screen_formats)
        
    url=soup.select("li>a.img")
    for i in url:
        urls1.append("https://www.miramarcinemas.tw/"+i.get('href'))

    for urlz in urls1:
        r = requests.get(urlz)
        soup = BeautifulSoup(r.text, 'html.parser')
        cast_items = soup.find('ul',class_="movie_info_item") 
        for item in cast_items:
            text = item.get_text(strip=True) 
            if "類型 GENRE" in text:
                movetype.append(text.replace("類型 GENRE", "").strip())  
            if "演員CAST" in text:  
                cast.append(text.replace("演員CAST", "").strip())
        # time=soup.select("div.movie_info>p.time")
        # for i in time:
        #     times.append((i.text.replace("片長:", "").strip())) 
        time=soup.find('p',class_="time")
        times.append((time.text.replace("片長:", "").strip()))     
        # Preview=soup.select("div.col.m6.s12.block>a")
        # for i in Preview:
        #     Previewurl.append(i['href'])
        Preview=soup.find('a',class_="btn_link left")
        if Preview==None:
                Previewurl.append('null')
        else:
            Previewurl.append(Preview['href'])
        # sjr=soup.select("div.col.m6.s12")
        # for sjrs in sjr:
        #     text = sjrs.get_text(strip=True)
        #     if "劇情簡介:" in text:
        #         movsj.append((text.replace("assignment劇情簡介:", "").strip()))
        sjr=soup.find('div',class_="col m6 s12")
        movsj.append((sjr.text.replace("assignment劇情簡介:", "").strip()))

    soup=get_soup("https://www.miramarcinemas.tw/Movie/Index?type=coming") #即將上映
    for movie_item in soup.find_all('li', class_='col s6 m4 l3'):
        # 取得電影名稱
        movie_name = movie_item.find('div', class_='title').contents[0].strip() 
        moviename.append(movie_name)
        # 取得電影海報網址
        poster_url = movie_item.find('a', class_='img').find('img')['src']
        movieposterurl.append(poster_url)
        # 取得上映日期
        release_date = movie_item.find('span', class_='date').get_text(strip=True)
        movieupday.append(release_date)
        # 取得畫面格式
        screen_formats = ', '.join([badge.get_text(strip=True) for badge in movie_item.find('div', class_='badge_area').find_all('a')])
        moviescreen.append(screen_formats)
    url=soup.select("li>a.img")
    for i in url:
        urls2.append("https://www.miramarcinemas.tw/"+i.get('href'))


    for urlz in urls2:
        soup=get_soup(urlz)
        cast_items = soup.find('ul',class_="movie_info_item") 
        for item in cast_items:
            text = item.get_text(strip=True)  
            if "類型 GENRE" in text:
                movetype.append(text.replace("類型 GENRE", "").strip())  
            if "演員CAST" in text: 
                cast.append(text.replace("演員CAST", "").strip())
        # time=soup.select("div.movie_info>p.time")
        # for i in time:
        #     times.append((i.text.replace("片長:", "").strip()))     
        time=soup.find('p',class_="time")
        times.append((time.text.replace("片長:", "").strip()))     
        # Preview=soup.select("div.col.m6.s12.block>a")
        # if len(Preview)==0:
        #         Previewurl.append('null')
        # else:
        #     for i in Preview:
        #         Previewurl.append(i['href'])
        Preview=soup.find('a',class_="btn_link left")
        if Preview==None:
                Previewurl.append('null')
        else:
            Previewurl.append(Preview['href'])
        # sjr=soup.select("div.col.m6.s12")
        # for sjrs in sjr:
        #     text = sjrs.get_text(strip=True)
        #     if "劇情簡介:" in text:
        #         movsj.append((text.replace("assignment劇情簡介:", "").strip()))
        sjr=soup.find('div',class_="col m6 s12")
        movsj.append((sjr.text.replace("assignment劇情簡介:", "").strip()))
        
    for a in zip(moviename,movieposterurl,movieupday,Previewurl,movetype,cast,movsj,times,moviescreen):
        totle.append(list(a))

    data=pd.DataFrame(totle,columns=["電影名稱", "電影海報網址", "上或待上映","電影預告網址","影片類型","主要演員","電影介紹","電影時長","電影螢幕"])
    # data.to_csv("mlfmovie.csv",index=False,)
    return data

def get_showTimeInfo():
    soup=get_soup("https://www.miramarcinemas.tw/Timetable/Index?cinema=standard") #上映

    total=[]
    title=soup.find_all('div',class_='title')
    papa=soup.find_all('div',class_='timetable_list row')
    for papas,titles in zip(papa,title):
        if titles.text in papas.text:
            soup = BeautifulSoup(papas.prettify(), 'html.parser')
            dates = soup.find_all('a', class_='booking_date')
            # print(titles.text)
            for date in dates:
                # 從 id 中獲取電影編號和日期（去掉 'a_' 前綴）
                session_id = date['id'].split('_')[1]
                full_date = date['id'].split('_')[2]  # 例如: 10月11日
                date_text=str(datetime.now().year)+"-"+full_date.replace('月','-').replace('日','')
                # 查找對應的場次區塊
                session_div = soup.find('div', class_=f"block {session_id} {full_date}")
            
                if session_div:
                    # 抓取電影名稱

                    # 抓取廳位類型 (如: 標準廳 或 IMAX)
                    room = (session_div.find('div', class_='room').get_text(strip=True)).replace("watch_later","")
                    if room!="IMAX":  #美麗華有特殊影廳 為了歸類方便 只分兩種
                        rooms="標準聽"
                    else:
                        rooms="IMAX"
                    # 抓取場次時間
                    times = session_div.find_all('a', class_='booking_time')
                    for time in times:
                        time_text = time.get_text(strip=True)
                    total.append([titles.text,"美麗華影城",date_text,time_text,rooms])

    data=pd.DataFrame(total,columns=["電影名稱","影城","日期","時間","廳位席位"])
    # data.to_csv("mlfmovietisr.csv",index=False,)
    return data

def get_theater():
    import pandas as pd
    x=[['美麗華影城','美麗華影城','台北市中山區敬業三路22號6樓','02-8502-2208']]

    data=pd.DataFrame(x,columns=['戲院名稱','影城','影城位置','影城電話'])
    return data

if __name__=="__main__":
    # print(get_movie())
    print(get_showTimeInfo())
    # print(get_theater())
    
