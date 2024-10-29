import pandas as pd
from bs4 import BeautifulSoup
import time, random, os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import threading, queue

movie_queue = queue.Queue()
show_queue = queue.Queue()

data = pd.DataFrame()


def setup_driver():
    chrome_options = Options()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")  # 無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    return webdriver.Chrome(service=chrome_service, options=chrome_options)


### 一部電影資訊
def scrape_one_movies(i, total_movies):
    # 重新獲取電影連結列表
    driver = setup_driver()
    driver.get("https://www.showtimes.com.tw/programs")

    # 等待電影海報元素加載
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-hCPjZK"))
    )
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
        print(f"成功抓取 {movie_data['電影名稱']} 的資料")

    except Exception as e:
        print(f"抓取數據時發生錯誤: {str(e)}")
        return

    finally:
        driver.close()
        return movie_queue.put(movie_data)


### 所有電影資訊
def scrape_all_movies():
    url = "https://www.showtimes.com.tw/programs"
    driver = setup_driver()
    threads = []
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
        running = 0
        for i in range(total_movies):
            if running >= 3:
                for thread in threads[i - running : i]:
                    thread.join()
                    running = 0

            crawl_thread = threading.Thread(
                target=scrape_one_movies, args=(i, total_movies)
            )
            crawl_thread.start()
            threads.append(crawl_thread)
            running += 1

        for thread in threads:
            all_movies_data.append(movie_queue.get())

        # 將所有數據轉換為DataFrame
        data = pd.DataFrame(all_movies_data)
        print("\n所有電影資料:")
        print(data)

        return data

        # # 保存到CSV
        # df.to_csv("showtimes_movie_data.csv", index=False, encoding='utf-8-sig')
        # print("\n資料已保存到 showtimes_movie_data.csv")

    except Exception as e:
        print(f"發生錯誤: {str(e)}")
    finally:
        driver.quit()


### 單部電影場次
def scrape_one_info(i, total_movies):
    try:
        url = "https://www.showtimes.com.tw/programs"
        driver = setup_driver()
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-hCPjZK"))
        )

        show_infos = []
        # 重新獲取電影連結列表
        movie_links = driver.find_elements(By.CLASS_NAME, "sc-dcJsrY")

        # 等待元素可點擊
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "sc-dcJsrY"))
        )

        print(f"正在處理第 {i+1}/{total_movies} 部電影")
        movie_links[i].click()
        time.sleep(3)

        element = WebDriverWait(driver, 15).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "sc-ihgnxF"), "選取影城")
        )
        title_element = driver.find_element(
            By.XPATH, '//*[@id="app"]/div/div[4]/div/div/div[2]/div[1]'
        )
        title = title_element.text

        cinemas = driver.find_elements(By.CLASS_NAME, "sc-iGgWBj")

        for cinema in cinemas:
            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "sc-iGgWBj"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", cinema)
                cinema_name = cinema.text
                if cinema_name == "更多…":
                    continue

                driver.execute_script("arguments[0].click();", cinema)

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "sc-iMTnTL"))
                )

                infos = driver.find_elements(By.CLASS_NAME, "sc-iMTnTL")
                for info in infos:
                    try:
                        date_text = info.text
                        date_text = (
                            str(datetime.now().year)
                            + "-"
                            + date_text.split("\n")[0]
                            .replace("月", "-")
                            .replace("日", "")
                        )
                        driver.execute_script("arguments[0].click();", info)
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "sc-gFVvzn"))
                        )

                        hall_elements = driver.find_elements(By.CLASS_NAME, "sc-gFVvzn")
                        time_elements = driver.find_elements(By.CLASS_NAME, "sc-fvtFIe")
                        for hall, time_element in zip(hall_elements, time_elements):
                            hall_text = hall.text.split("\n")
                            if len(hall_text) >= 3:
                                hall_info = (
                                    f"{hall_text[0]}{hall_text[1]}{hall_text[2]}"
                                )
                            elif len(hall_text) == 2:
                                hall_info = f"{hall_text[0]}{hall_text[1]}"
                            else:
                                hall_info = hall_text[0]
                            times = time_element.text.strip().split("\n")

                            for single_time in times:
                                if single_time and cinema_name:
                                    show_infos.append(
                                        {
                                            "電影名稱": title,
                                            "影城": cinema_name,
                                            "日期": date_text,
                                            "廳位席位": hall_info,
                                            "時間": single_time.strip("早優 "),
                                        }
                                    )

                    except Exception as e:
                        print(f"Error with date '{date_text}': {e}")
                        continue

            except Exception as e:
                print(
                    f"Error with cinema '{cinema_name if 'cinema_name' in locals() else 'Unknown'}': {e}"
                )

    except Exception as e:
        print(f"處理電影時發生錯誤: {str(e)}")

    finally:
        driver.close()
        print(i + 1, "處理完畢")
        return show_queue.put(show_infos)


### 所有電影場次
def scrape_show_info():
    data_list = []
    threads = []
    url = "https://www.showtimes.com.tw/programs"
    driver = setup_driver()

    try:
        # 訪問主頁面
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-dcJsrY"))
        )

        # 獲取所有電影連結
        movie_links = driver.find_elements(By.CLASS_NAME, "sc-dcJsrY")
        total_movies = len(movie_links)
        print(f"找到 {total_movies} 部電影")

        # 遍歷每個電影連結
        running = 0
        for i in range(total_movies):
            if running >= 3:
                for thread in threads[i - running : i]:
                    thread.join()
                    running = 0

            crawl_thread = threading.Thread(
                target=scrape_one_info, args=(i, total_movies)
            )
            crawl_thread.start()
            threads.append(crawl_thread)
            running += 1

        for thread in threads:
            data_list.extend(show_queue.get())

    except TimeoutException:
        print("", end="")

    finally:
        driver.quit()

    if data_list:
        data = pd.DataFrame(data_list)
        data["場次類型"] = None
        print(data)
        return data
    else:
        print("電影尚未公布場次")
        return pd.DataFrame()


### 所有戲院資訊
def scrape_cinema_info(url="https://www.showtimes.com.tw/info/cinema"):
    driver = setup_driver()
    driver.get(url)

    # 等待頁面加載
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "sc-kbdlSk"))
    )

    # 獲取頁面源碼
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, "html.parser")

    # 提取影院信息
    cinemas = []
    cinema_divs = soup.find_all("div", class_="sc-kbdlSk fgCmbm")
    for cinema_div in cinema_divs:
        name = cinema_div.text.strip()
        info_divs = cinema_div.find_next_siblings("div", class_="sc-camqpD lmjUEm")
        location = info_divs[0].text.strip() if len(info_divs) > 0 else "N/A"
        phone = info_divs[1].text.strip() if len(info_divs) > 1 else "N/A"

        cinemas.append(
            {
                "戲院名稱": name,
                "影城": "秀泰影城",
                "影城位置": location,
                "影城電話": phone,
            }
        )

        # 隨機延遲0.5到2秒
        time.sleep(random.uniform(0.5, 2))

    driver.quit()
    return pd.DataFrame(cinemas)


if __name__ == "__main__":
    print(scrape_all_movies())
