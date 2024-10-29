# -*- coding: utf-8 -*-
"""
Created on Sat Oct 19 19:05:17 2024

@author: Barry
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from selenium import webdriver
from io import BytesIO
from PIL import Image
import base64,time,os
from datetime import datetime

def setup_driver():
    chrome_options = Options()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless") #無頭模式
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_service = Service(os.environ.get("CHROMEDRIVER_PATH"))
    return webdriver.Chrome(service=chrome_service,options=chrome_options)

def verify_CAPTCHA(driver): # 驗證我不是機器人，只要失敗就 refresh 網頁並重新驗證
    try:
        username = driver.find_element(By.NAME,"Account")
        username.send_keys("barrytruth@hotmail.com")
        pw = driver.find_element(By.NAME,"Password")
        pw.send_keys("Bb0933001127")
        WebDriverWait(driver, 3).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))) # 找到並切換到 reCAPTCHA 的 iframe
        captcha = driver.find_element(By.CLASS_NAME,"recaptcha-checkbox") # 找到 "我不是機器人" 的 checkbox
        driver.execute_script("arguments[0].click();", captcha)
        time.sleep(20)
        driver.switch_to.default_content() # 切換回主頁面
        login_btn = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.ID, "btnLogin")))
        login_btn.click()
    except:
        driver.refresh() # refresh 網頁
        verify_CAPTCHA(driver) # 重新驗證

def miramarSeat(theater_name,movie_name,movie_date,movie_room,movie_session):
    emptySeat = []
    bookedSeat = []
    movie_date = movie_date.strftime('%m月%d日 星期') + ["一", "二", "三", "四", "五", "六", "日"][movie_date.weekday()]

    try:
    
        for i,m_session in zip(range(len(movie_session)),movie_session):

            if movie_session == [""]:
                emptySeat = ""
                bookedSeat = ""
                seatImage = ""
                continue

            if i == 0:
                login_addr = "Member/Login"
                main_page = "https://www.miramarcinemas.tw/"

                driver = setup_driver()
                ############################# 起始斷頭模式動態網頁方式，並取得網頁資料 #############################
                # options = webdriver.ChromeOptions()
                # options.add_argument("--headless")
                # driver = webdriver.Chrome(options=options)
                # # driver = webdriver.Chrome() # 非斷頭模式
                driver.maximize_window()
                ############################################ 會員登入 ############################################
                driver.get(main_page+login_addr)
                
                ################ 點選-我不是機器人 ################
                verify_CAPTCHA(driver)
                ##################################################
                
                alert = WebDriverWait(driver, 10).until(EC.alert_is_present()) # 等待 alert 彈出視窗出現
                alert = driver.switch_to.alert # 切換到 alert 視窗
                alert.accept()
                time.sleep(2)
                ##################################################################################################
            else:
                driver.back()
                driver.back()
            ########################################### 進入選擇頁 ###########################################
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"sel_cinema")))
            cinema = Select(driver.find_element(By.ID,"sel_cinema"))
            cinema.select_by_visible_text(theater_name)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"sel_movie")))
            movie = Select(driver.find_element(By.ID,"sel_movie"))
            movie.select_by_visible_text(movie_name)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"sel_show_time")))
            date = Select(driver.find_element(By.ID,"sel_show_time"))
            date.select_by_visible_text(movie_date)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"sel_show_session")))
            session = Select(driver.find_element(By.ID,"sel_show_session"))
            session.select_by_visible_text(m_session)
            seat_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,"waves-effect")))
            seat_btn.click()
            
            ########################################### 進入訂票頁 ###########################################
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"ticket_type_select_0147")))
            tckt = Select(driver.find_element(By.ID,"ticket_type_select_0147"))
            tckt.select_by_value("1")  
            
            next_btn = driver.find_element(By.CLASS_NAME,"waves-effect")
            driver.execute_script("arguments[0].click();", next_btn) # 要用 Java 的 .click() 點擊

            ########################################### 讀進座位表 ###########################################
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME,"seat_booking_block")))
            seat_raw = driver.page_source
            soop = BeautifulSoup(seat_raw,"html.parser")
            table= soop.select("div.seat_booking_block td")
            
            eSeat = -1 # 就是空位數；因為螢幕也有一個 "white"，所以要扣掉 1
            bSeat = 0 # 就是總座位數
            
            for i in table:
                if "background-color:white" in str(i):
                    eSeat += 1
                elif "background-color:gray" in str(i):
                    bSeat += 1
            
            emptySeat.append(eSeat)
            bookedSeat.append(bSeat)
            

            if len(movie_session) == 1:
                ########################################### 座位表區截圖 ###########################################
                seat_map = driver.find_element(By.ID, 'seatTable')
                driver.execute_script("document.getElementById('inav').style.display='none';") # 由於截圖時，上方有橫幅會擋到圖，因此這裡將橫幅隱藏
                driver.execute_script("arguments[0].scrollIntoView(true);",seat_map)
                time.sleep(0.5)
                # 使用 selenium 的 get_screenshot_as_png 獲取圖的二進位數據
                image_data = seat_map.screenshot_as_png  # 這將返回 PNG 格式的二進位數據
                # 使用 BytesIO 將截圖的二進位數據儲存至RAM
                image_stream = BytesIO(image_data)
                image_stream.seek(0)
                # 使用 PIL 打開RAM中的圖
                image = Image.open(image_stream)
                # 將圖轉換為 base64 格式
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                seatImage = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')
            else:
                seatImage = ""
        
        if movie_session != [""]:
            driver.quit()        
        return emptySeat, bookedSeat, seatImage
    finally:
        driver.quit()

def showtimeSeat(theater_name,movie_name,movie_date,movie_room,movie_session):
    emptySeat = []
    bookedSeat = []
    movie_date = movie_date.strftime('%m月%d日')

    try:
    
        for z,m_room,m_session in zip(range(len(movie_session)),movie_room,movie_session):    

            m_room = m_room.lstrip(theater_name) # 專案中的電影爬蟲給的影廳是前面帶有戲院名稱的，所以這裡要刪除掉        

            if movie_session == [""]:
                emptySeat = ""
                bookedSeat = ""
                seatImage = ""
                continue

            if z == 0:
                main_page = "https://www.showtimes.com.tw/"
                choose_addr = "programs/"

                driver = setup_driver()
                
                ############################# 起始斷頭模式動態網頁方式，並取得網頁資料 #############################
                # chrome_options = Options()
                # chrome_options.add_argument("--headless") #無頭模式
                # chrome_options.add_argument("--disable-dev-shm-usage")
                # chrome_options.add_argument("--disable-gpu")
                # chrome_options.add_argument("--no-sandbox")
                # chrome_service = Service(os.environ.get("CHROMEDRIVER_PATH"))
                # driver = webdriver.Chrome(options=options)
                # driver = webdriver.Chrome() # 非斷頭模式
                driver.maximize_window()
                ########################################### 進入座位表 ###########################################

            driver.get(main_page+choose_addr)
                

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "sc-gFAWRd")))
            # 選電影
            sel_btn_m = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(text(), '{movie_name}')]/ancestor::div[2]/following-sibling::div[contains(@class, 'sc-iHbSHJ')]")))
            driver.execute_script("arguments[0].click();", sel_btn_m)
            # 選戲院
            sel_btn_th = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{theater_name}')]")))
            driver.execute_script("arguments[0].click();", sel_btn_th)
            # 選日期
            sel_btn_d = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{movie_date}')]")))
            driver.execute_script("arguments[0].click();", sel_btn_d)
            # 選場次
            sel_btn_s = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(normalize-space(), '{m_room}')]/following-sibling::div//button[contains(text(), '{m_session}')]")))
            driver.execute_script("arguments[0].click();", sel_btn_s)
            
            ########################################### 彈出視窗 ###########################################
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary")))
            cfm = driver.find_elements(By.CLASS_NAME,"btn-primary")
            driver.execute_script("arguments[0].click();", cfm[2])
            ###############################################################################################
            
            # 選訂票張數
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "form-control")))
            sel_btn_tk = Select(driver.find_elements(By.CLASS_NAME,"form-control")[0]) # 找出所有票種的選單，並選擇第1個票種的選單(有的電影只有一種票)
            sel_btn_tk.select_by_value("1")   # 選擇1張票
            
            # 按下[開始選取座位]按鈕
            seat_btn = driver.find_element(By.CLASS_NAME,"sc-fBdRDi")
            seat_btn.click()
            
            ########################################### 彈出視窗 ###########################################
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "site-modal")))
            cfm_f = driver.find_elements(By.CLASS_NAME,"btn-primary")
            driver.execute_script("arguments[0].click();", cfm_f[1])
            #################### 等網頁更新、有Class = sc-iHmpnF 後，再開始獲取網頁作解析 ####################
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "sc-iHmpnF")))
            seatInfo = driver.page_source
            soop = BeautifulSoup(seatInfo,"html.parser")
            ########################################### 座位資料處理 ###########################################
            table = soop.select("div.sc-iHmpnF")
            eSeat = 0
            bSeat = 0
            
            for j,i in zip(range(len(table)),table):
                if len(i.text) == 0 or i.text.isdigit() == False or "hXhSKb" in str(i):
                    continue
                else:
                    if "gpujMZ" in str(i):
                        eSeat += 1
                    elif "iCXUVq" in str(i):
                        bSeat +=1
            
            emptySeat.append(eSeat)
            bookedSeat.append(bSeat)
            
            if len(movie_session) == 1:
                ########################################### 座位表區截圖 ###########################################
                seat_map = driver.find_element(By.CLASS_NAME, 'sc-ehixzo')
                driver.execute_script("arguments[0].scrollIntoView(true);",seat_map)
                time.sleep(0.5)
                # 使用 selenium 的 get_screenshot_as_png 獲取圖的二進位數據
                image_data = seat_map.screenshot_as_png  # 這將返回 PNG 格式的二進位數據
                # 使用 BytesIO 將截圖的二進位數據儲存至RAM
                image_stream = BytesIO(image_data)
                image_stream.seek(0)
                # 使用 PIL 打開RAM中的圖
                image = Image.open(image_stream)
                # 將圖轉換為 base64 格式
                buffered = BytesIO()
                image.save(buffered, format="PNG")
                seatImage = "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')
            else:
                seatImage = ""

        if movie_session != [""]:
            driver.quit()
        return emptySeat, bookedSeat, seatImage
    finally:
        driver.quit()


def findSeats(theater_name,movie_name,movie_date,movie_room,movie_session):
    if "秀泰" in theater_name:
        emptySeat, bookedSeat, seatImage = showtimeSeat(theater_name,movie_name,movie_date,movie_room,movie_session)
    elif "美麗華" in theater_name:
        emptySeat, bookedSeat, seatImage = miramarSeat(theater_name,movie_name,movie_date,movie_room,movie_session)
    else:
        return '暫無資料','暫無資料','暫無資料'
    return emptySeat, bookedSeat, seatImage