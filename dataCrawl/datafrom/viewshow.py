"""
funtion 暫定
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []


def movie(url, mmm):
    aa = requests.get(url)
    soup = BeautifulSoup(aa.text, "html.parser")
    theaterMode = {}
    theaterTime = {}
    theaterCode = {}
    ul = soup.find("ul", "versionList")
    for i in ul.find_all("li"):  # 抓劇院編號
        if i.a["href"] == "#":
            theaterMode[i.a.text] = []
            modeName = i.a.text
        else:
            theaterCode[i.a.text] = i.a["href"]
            theaterMode[modeName].append(i.a.text)
    for i in theaterCode:
        theaterTime[i] = []
    # -------------------------
    for name in theaterCode:  # 建時刻表
        d1 = {}
        dd = theaterCode[name][1:]
        aa = soup.find("article", id=f"{dd}")
        for i in aa.find_all("div", "movieDay"):
            # print(i.h4.text)
            d1[i.h4.text] = []
            for time in i.find_all("li"):
                theaterTime[name].append({(i.h4.text): (time.a.text)})
    # -------------------------
    for m1 in theaterMode:  # 從電影放映版本抓影城
        mode = m1  # 放映版本
        for aa in range(len(theaterMode[m1])):
            theaterName = theaterMode[m1][aa]  # 影城
            for a1 in theaterTime[theaterName]:
                keys = set(a1.keys())
                for i in keys:
                    movieDay = (
                        i.replace(" 年 ", "-").replace(" 月 ", "-").split(" 日")[0]
                    )  # 日期
                    movieTime = a1[i]  # 時間
                    total = [mmm, mode, theaterName, movieDay, movieTime]
                    data.append(total)


movieName1 = {}


def pg(url):
    aa = requests.get(url)
    soup = BeautifulSoup(aa.text, "html.parser")
    s1 = soup.find("ul", "movieList")

    for i in s1.find_all("li"):  # 抓電影網址
        movieName1[i.find("h2").text] = (
            "https://www.vscinemas.com.tw/vsweb/film/" + i.find("h2").a["href"]
        )


def get_datas():
    aa = requests.get("https://www.vscinemas.com.tw/vsweb/film/index.aspx")
    soup = BeautifulSoup(aa.text, "html.parser")
    s1 = soup.find("section", "pagebar").ul
    page = []
    for i in s1.find_all("a"):
        if i.get("href"):
            page.append(
                "https://www.vscinemas.com.tw/vsweb/film/index.aspx" + i.get("href")
            )
    for pa in page:  # 頁數
        pg(pa)
    for i in movieName1:
        movie(movieName1[i], i)
    datas = pd.DataFrame(data, columns=["電影名稱", "廳位席位", "影城", "日期", "時間"])
    datas["場次類型"] = None
    return datas
    # with open("output.csv", mode="w", newline="", encoding="utf-8-sig") as file:
    #     writer = csv.writer(file)
    #     # 寫入每一列
    #     writer.writerows(data)


if __name__ == "__main__":
    print(get_datas())
