import pandas as pd
import requests
from bs4 import BeautifulSoup
import threading,queue

datas=pd.DataFrame()

movie_queue=queue.Queue()
show_queue=queue.Queue()

def get_soup(url):
    r=requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

finall=[] #彙總
movietisr=[]
posturl=[]

def get_one_movie(url):
    global finall,movietisr
    soups=get_soup(url)
    titles = soups.select('div.cell.small-12.medium-12.large-12.movie-info-box>h2')
    #titles[0].text電影名稱
    title=titles[0].text
    posturls=soups.select('div>img')
    #posturl[0].get('src')海報網址
    posturl=posturls[0].get('src')
    sjcotyday= soups.select('div.cell.small-12.medium-12.large-12.movie-info-box>p')
    #sjcotyday[0].text電影介紹
    sj=sjcotyday[0].text
    #sjcotyday[1].text主要演員：
    cost=sjcotyday[1].text.replace("主要演員：","") if sjcotyday[1].text.replace("主要演員：","") else "null"
    #sjcotyday[2].text影片類型：
    types=sjcotyday[2].text.replace("影片類型：","") if sjcotyday[2].text.replace("影片類型：","") else "null"
    #sjcotyday[3].text上映日期：
    upday=sjcotyday[3].text.replace("上映日期：","")if sjcotyday[3].text.replace("上映日期：","") else "null"
    time=soups.select('div.rating-box>span')
    #time[1].text電影時間
    if len(time) > 1:
        motime = time[1].text
    elif len(time) == 1:
        motime = time[0].text
    else:
        motime = "null"
    
    seat=soups.select('div.theater-box>p.tag-seat')
    seats=set()
    for i in seat:
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
        date=date.replace('/','-')
        urls="https://www.ambassador.com.tw"+items.get('href')
        soups=get_soup(urls)
        for item in soups.select('div.theater-box'):
            lcmove=item.select("h3>a")[0].text
            locs=item.select("div.theater-box>h3>span")
            # times=item.select("li>h6")
            # seats=item.select("p>span.float-left.info")
            screenings = item.find_all('p', class_='tag-seat')
            for screening in screenings:
                movie_info = screening.get_text()
                times = screening.find_next('ul', class_='no-bullet').find_all('li')
                for time in times:
                    # 抓取時間
                    showtime = time.find('h6').get_text(strip=True)
                    # 抓取廳位和座位數
                    hall_seat_info = time.find('span', class_='info').get_text(strip=True)
            
                # for time,seat in zip(times,seats):
                    show_infos.append([title,lcmove,date,showtime,hall_seat_info,movie_info])
    return movie_queue.put(movie_datas),show_queue.put(show_infos)

    # finall.append(movie_datas)
    # movietisr.extend(show_infos)

    # return movie_datas,show_infos


def get_movie_and_show():
    # soup=get_soup('https://www.ambassador.com.tw/home/MovieList?Type=0')
    print('get_movie_and_show START')
    soup=get_soup('https://www.ambassador.com.tw/home/MovieList')
    urls=soup.select("div.cell>a.poster")
    threads=[]
    for a in urls:
        url="https://www.ambassador.com.tw"+a.get('href')
        crawl_thread=threading.Thread(target=get_one_movie,args=(url,))
        crawl_thread.start()
        threads.append(crawl_thread)

    for thread in threads:
        thread.join()
    
    for thread in threads:
        finall.append(movie_queue.get())
        movietisr.extend(show_queue.get())

    movie_datas=pd.DataFrame(finall,columns=["電影名稱", "電影海報網址", "上或待上映","電影預告網址","影片類型","主要演員","電影介紹","電影時長","電影螢幕"])
    show_datas=pd.DataFrame(movietisr,columns=["電影名稱","影城","日期","時間", "廳位席位","場次類型"])
    print('get_movie_and_show FINISH')
    print(show_datas)
    return movie_datas,show_datas
    


def get_theater():
    print('get_theater START')
    r=requests.get("https://www.ambassador.com.tw/home/TheaterList")
    soups = BeautifulSoup(r.text.split('<div class="fluid">')[0], 'html.parser')
    mourl=soups.select('div.grid-container div.cell > a')
    theaters=[]
    for items in mourl:
        title=items.find('h6').text.strip()
        address=items.find_all('p')[0].text.strip()
        phone=items.find_all('p')[1].text.strip()
        theaters.append([title,"國賓影城",address,phone])
        theaters.append([title,"國賓影城",address,phone])
    datas=pd.DataFrame(theaters,columns=["戲院名稱","影城", "影城位置", "影城電話"])
    print('get_theater FINISH')
    return datas
    


if __name__=="__main__":
    print(get_movie_and_show())
    # print(get_theater())
