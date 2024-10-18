import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
import random

def setup_driver():
    chrome_options = Options()
    return webdriver.Chrome(options=chrome_options)

### 電影資訊
def scrape_all_movies():
    url = "https://www.showtimes.com.tw/programs"
    driver = webdriver.Chrome()
    all_movies_data = []

    try:
        # 訪問主頁面
        driver.get(url)

        # 等待電影海報元素加載
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-hCPjZK"))
        )

        # 獲取所有電影連結
        movie_links = driver.find_elements(By.CLASS_NAME, "sc-dcJsrY")
        total_movies = len(movie_links)
        print(f"找到 {total_movies} 部電影")

        # 遍歷每個電影連結
        for i in range(total_movies):
            try:
                # 重新獲取電影連結列表
                movie_links = driver.find_elements(By.CLASS_NAME, "sc-dcJsrY")

                # 等待元素可點擊
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "sc-dcJsrY"))
                )

                print(f"正在處理第 {i+1}/{total_movies} 部電影")
                movie_links[i].click()
                time.sleep(3)

                try:
                    # 等待頁面加載並抓取數據
                    movie_data = {}

                    # 電影名稱
                    title = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (
                                By.XPATH,
                                '//*[@id="app"]/div/div[4]/div/div/div[2]/div[1]',
                            )
                        )
                    )
                    movie_data["電影名稱"] = title.text

                    # 電影類型
                    try:
                        movie_type = driver.find_element(
                            By.XPATH,
                            '//*[@id="app"]/div/div[4]/div/div/div[2]/div[7]/div[2]',
                        )
                        movie_data["電影類型"] = movie_type.text
                    except NoSuchElementException:
                        movie_data["電影類型"] = "未知"

                    # 主要演員
                    try:
                        movie_actor = driver.find_element(
                            By.XPATH,
                            '//*[@id="app"]/div/div[4]/div/div/div[2]/div[8]/div[2]',
                        )
                        movie_data["主要演員"] = movie_actor.text
                    except NoSuchElementException:
                        movie_data["主要演員"] = "未知"

                    # 電影介紹
                    try:
                        movie_introduction = driver.find_element(
                            By.XPATH,
                            '//*[@id="app"]/div/div[4]/div/div/div[2]/div[10]/div[2]/div/div/div',
                        )
                        movie_data["電影介紹"] = movie_introduction.text
                    except NoSuchElementException:
                        movie_data["電影介紹"] = "未知"

                    # 電影時長
                    try:
                        movie_time = driver.find_element(
                            By.XPATH,
                            '//*[@id="app"]/div/div[4]/div/div/div[2]/div[4]/div[2]',
                        )
                        movie_data["電影時長"] = movie_time.text
                    except NoSuchElementException:
                        movie_data["電影時長"] = "未知"

                    movie_data["電影海報網址"] = "未知"
                    movie_data["電影預告網址"] = "未知"
                    movie_data["影片類型"] = "未知"
                    movie_data["上或待上映"] = "未知"

                    all_movies_data.append(movie_data)
                    print(f"成功抓取 {movie_data['電影名稱']} 的資料")

                except Exception as e:
                    print(f"抓取數據時發生錯誤: {str(e)}")

                # 返回主頁面
                driver.back()
                time.sleep(3)

                # 等待主頁面重新加載
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sc-hCPjZK"))
                )

            except Exception as e:
                print(f"處理電影時發生錯誤: {str(e)}")
                continue

        # 將所有數據轉換為DataFrame
        df = pd.DataFrame(all_movies_data)
        print("\n所有電影資料:")
        print(df)

        return df

        # # 保存到CSV
        # df.to_csv("showtimes_movie_data.csv", index=False, encoding='utf-8-sig')
        # print("\n資料已保存到 showtimes_movie_data.csv")

    except Exception as e:
        print(f"發生錯誤: {str(e)}")
    finally:
        driver.quit()


### 戲院資訊
def scrape_cinema_info(url='https://www.showtimes.com.tw/info/cinema'):
    driver = setup_driver()
    driver.get(url)
    
    # 等待頁面加載
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-kbdlSk"))
    )
    
    # 獲取頁面源碼
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # 提取影院信息
    cinemas = []
    cinema_divs = soup.find_all('div', class_='sc-kbdlSk fgCmbm')
    for cinema_div in cinema_divs:
        name = cinema_div.text.strip()
        info_divs = cinema_div.find_next_siblings('div', class_='sc-camqpD lmjUEm')
        location = info_divs[0].text.strip() if len(info_divs) > 0 else 'N/A'
        phone = info_divs[1].text.strip() if len(info_divs) > 1 else 'N/A'
        
        cinemas.append({
            "戲院名稱": name,
            '影城': '秀泰影城',
            '影城位置': location,
            '影城電話': phone
        })
        
        # 隨機延遲0.5到2秒
        time.sleep(random.uniform(0.5, 2))
    
    driver.quit()
    return pd.DataFrame(cinemas)






if __name__ == "__main__":
    print(scrape_all_movies())
    # 使用函數
    url = 'https://www.showtimes.com.tw/info/cinema'
    df = scrape_cinema_info(url)
    print(df)

    df.to_csv("sohwtimes位置.csv" ,index=False ,encoding="utf-8-sig")
