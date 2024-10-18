### 宏碁電影整合系統

目前進度：

資料庫：
已成功整合以下爬找：
電影：美麗華、國賓、秀泰
影廳：美麗華、國賓、秀泰
電影座位資訊：美麗華、國賓

資料上傳database可於console端輸入以下指令進行測試：
- python manage.py upload_database --model movies
- python manage.py upload_database --model theaters
- python manage.py upload_database --model shows

首頁查詢系統：已初步完成
電影資訊頁面：已初步完成，正在整合評論系統
影院資訊頁面：進行中
訂購系統：進行中，正在整合地圖顯示
