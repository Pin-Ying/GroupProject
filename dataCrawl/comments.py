# from .models import movie
from user.models import Review, Movie, User
import pandas as pd
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# 清空評論資料表並導入新資料
def import_reviews():

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    # url = "https://today.line.me/tw/v2/comment/movie/Kw8pGwr"
    # driver.get(url)
    time.sleep(5)  # Adjust the sleep time if necessary
    page_source = driver.page_source

    url = "https://today.line.me/tw/v2/movie/chart/trending"
    driver.get(url)
    time.sleep(5)
    page_source = driver.page_source
    soups = BeautifulSoup(page_source, "html.parser")
    movieDict = {}

    href = []
    a1 = soups.find_all("a", "detailListItem-bookingButton")
    for i in a1:
        # print(i["href"])
        href.append("https://today.line.me" + i["href"])
    comment = {}
    for i in range(len(href)):
        co = []
        hre = href[i]
        driver.get(hre)
        time.sleep(5)
        page_source = driver.page_source
        soups = BeautifulSoup(page_source, "html.parser")
        name1 = soups.find("div", "filmLiteCard-title")
        comment[name1.text] = []
        a1 = soups.find_all("div", "commentItem-content")

        for i in a1:
            comment[name1.text].append(i.text)
    data = {"電影名稱": [], "評論": []}
    for i in comment:
        for j in comment[i]:
            data["電影名稱"].append(i)
            data["評論"].append(j)

    df = pd.DataFrame(data)
    user = User.objects.get(name="LineMoviesComments")
    for index, row in df.iterrows():
        try:
            movie_data = Movie.objects.get(title=row["電影名稱"])
        except movie_data.DoesNotExist:
            print(f"電影 '{row['電影名稱']}' 在數據庫中不存在，跳過該排片。")
            continue  # 如果電影不存在，跳過當前行
        review, created = Review.objects.get_or_create(user=user,movie=movie_data, content=row["評論"]
        )
