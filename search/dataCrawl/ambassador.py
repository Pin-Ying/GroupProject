import pandas as pd
import requests
from bs4 import BeautifulSoup
import threading

def get_soup(url):
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

finall=[] #彙總
movietisr=[]
posturl=[]

def get_one_movie(url):
    soups=get_soup(url)
    title = soups.select('div.cell.small-12.medium-12.large-12.movie-info-box>h2')[0].text
    posturl=soups.select('div>img')[0].get('src')
    sjcotyday= soups.select('div.cell.small-12.medium-12.large-12.movie-info-box>p')
    # 電影介紹
    sj=sjcotyday[0].text
    # 主要演員
    cost=sjcotyday[1].text.replace("主要演員：","") if sjcotyday[1].text.replace("主要演員：","") else "null"
    # 影片類型
    types=sjcotyday[2].text.replace("影片類型：","") if sjcotyday[2].text.replace("影片類型：","") else "null"
    # 上映日期
    upday=sjcotyday[3].text.replace("上映日期：","")if sjcotyday[3].text.replace("上映日期：","") else "null"
    time=soups.select('div.rating-box>span')
    # 電影時間
    if len(time) > 1:
        motime = time[1].text
    elif len(time) == 1:
        motime = time[0].text
    else:
        motime = "null"
    
    seat=soups.select('div.theater-box>p.tag-seat')
    seats=set()
    for i in seat:
        if "數位" in i.text:
            seats.add("數位")
        if "3D" in i.text:
            seats.add("3D")
        if "IMAX" in i.text:
            seats.add("IMAX")
    seats=list(seats)
    movie_datas=[title,posturl,upday,'null',types,cost if cost else "null",
                    sj,motime,seats]

    show_infos=[]
    mourl=soups.select('section>div>div>div>ul>li>ul>li>a')
    #https://www.ambassador.com.tw/
    for items in mourl:
        date=items.get('href').split("DT=")[1]
        urls="https://www.ambassador.com.tw"+items.get('href')
        soups=get_soup(urls)
        for item in soups.select('div.theater-box'):
            lcmove=item.select("h3>a")[0].text
            times=item.select("li>h6")
            seats=item.select("p>span.float-left.info")
            
            for time,seat in zip(times,seats):
                show_infos.append([title,lcmove,date,time.text.strip(),seat.text])

    return movie_datas,show_infos


def get_movie_and_show():
    soup=get_soup('https://www.ambassador.com.tw/home/MovieList?Type=0')
    urls=soup.select("div.cell>a.poster")
    for a in urls:
        url="https://www.ambassador.com.tw"+a.get('href')
        movie_datas,show_infos=get_one_movie(url)
        finall.append(movie_datas)
        movietisr.extend(show_infos)
    movie_datas=pd.DataFrame(finall,columns=["電影名稱", "電影海報網址", "上或待上映","電影預告網址","影片類型","主要演員","電影介紹","電影時長","電影螢幕"])
    movie_datas=pd.DataFrame(movietisr,columns=["電影名稱","影城","日期","時間", "廳位席位"])

    return movie_datas,movie_datas
    


def get_theater():
    r=requests.get("https://www.ambassador.com.tw/home/TheaterList")
    soups = BeautifulSoup(r.text.split('<div class="fluid">')[0], 'html.parser')
    mourl=soups.select('div.grid-container div.cell > a')
    theaters=[]
    for items in mourl:
        title=items.find('h6').text.strip()
        address=items.find_all('p')[0].text.strip()
        phone=items.find_all('p')[1].text.strip()
        theaters.append(["國賓影城",title,address,phone])
    datas=pd.DataFrame(theaters,columns=["戲院名稱","影城", "影城位置", "影城電話"])
    return datas
    


# # soup=get_soup('https://www.ambassador.com.tw/home/MovieList?Type=0')
# soup=get_soup('https://www.ambassador.com.tw/home/MovieList?Type=0')
# url=soup.select("div.cell>a.poster")
# for i in url:
#     urls="https://www.ambassador.com.tw"+i.get('href')
#     soups=get_soup(urls)
#     titles = soups.select('div.cell.small-12.medium-12.large-12.movie-info-box>h2')
#     #titles[0].text電影名稱
#     title=titles[0].text
#     posturls=soups.select('div>img')
#     #posturl[0].get('src')海報網址
#     posturl=posturls[0].get('src')
#     sjcotyday= soups.select('div.cell.small-12.medium-12.large-12.movie-info-box>p')
#     #sjcotyday[0].text電影介紹
#     sj=sjcotyday[0].text
#     #sjcotyday[1].text主要演員：
#     cost=sjcotyday[1].text.replace("主要演員：","") if sjcotyday[1].text.replace("主要演員：","") else "null"
#     #sjcotyday[2].text影片類型：
#     types=sjcotyday[2].text.replace("影片類型：","") if sjcotyday[2].text.replace("影片類型：","") else "null"
#     #sjcotyday[3].text上映日期：
#     upday=sjcotyday[3].text.replace("上映日期：","")if sjcotyday[3].text.replace("上映日期：","") else "null"
#     time=soups.select('div.rating-box>span')
#     #time[1].text電影時間
#     if len(time) > 1:
#         motime = time[1].text
#     elif len(time) == 1:
#         motime = time[0].text
#     else:
#         motime = "null"
    
#     seat=soups.select('div.theater-box>p.tag-seat')
#     seats=set()
#     for i in seat:
#         if "數位" in i.text:
#             seats.add("數位")
#         if "3D" in i.text:
#             seats.add("3D")
#         if "IMAX" in i.text:
#             seats.add("IMAX")
#     seats=list(seats)
#     finall.append([title,posturl,upday,'null',types,cost if cost else "null",
#                    sj,motime,seats])
    
    # mourl=soups.select('section>div>div>div>ul>li>ul>li>a')
    # #https://www.ambassador.com.tw/
    # for items in mourl:     
    #     urls="https://www.ambassador.com.tw"+items.get('href')
    #     soups=get_soup(urls)
    #     for item in soups.select('div.theater-box'):
    #         lcmove=item.select("h3>a")
    #         # lcmove[0].text 台北長春國賓影城
    #         time=item.select("li>h6")
    #         #.strip()
    #         sets=item.select("p>span.float-left.info")
    #         for i,j in zip(time,sets):
    #             # print(i.text,j.text,lcmove[0].text)
    #             movietisr.append([titles[0].text,lcmove[0].text,(items.text)[-10:],i.text.strip(),j.text])
            
    #         locs=item.select("div.theater-box>h3>span")
    #         loc.add(("國賓影城",lcmove[0].text,locs[0].text,locs[2].text))

# data=pd.DataFrame(movietisr,columns=["電影名稱","影城","日期","時間", "廳位席位"])
# data.to_csv("gobimovieti.csv",index=False,)
# data=pd.DataFrame(finall,columns=["電影名稱", "電影海報網址", "上或待上映","電影預告網址","影片類型","主要演員","電影介紹","電影時長","電影螢幕"])
# data.to_csv("gobimovie.csv",index=False,)
# locator=(By.ID,'recommend')

if __name__=="__main__":
    print(get_movie_and_show())
    # print(get_theater())
