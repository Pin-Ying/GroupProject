from myapp.showtime import showtimeSeat
from django.shortcuts import render
from django.conf import settings
import pandas as pd
from datetime import date
import os
from flask import Flask, render_template, request, redirect, url_for

today = date.today()
today_text = today.strftime("%m月%d日")

theater1 = "台中站前秀泰"
movie_name1 = "荒野機器人"
movie_date1 = "10月17日"
movie_room1 = "1館8廳"
movie_session1 = "21:00"
pic_folder = settings.MEDIA_ROOT + "\\"

m_sessions = pd.DataFrame(
    {
        "room": [
            "1館7廳",
            "1館7廳",
            "1館7廳",
            "1館7廳",
            "1館7廳",
            "1館7廳",
            "1館7廳",
            "1館8廳",
            "1館8廳",
            "1館8廳",
            "1館8廳",
            "1館8廳",
            "1館8廳",
            "1館8廳",
        ],
        "session": [
            "10:00",
            "14:00",
            "18:00",
            "20:00",
            "22:00",
            "12:00",
            "16:00",
            "14:00",
            "17:00",
            "21:00",
            "23:00",
            "11:00",
            "15:00",
            "19:00",
        ],
    }
)


def seats(request):
    # 检查表单提交的影厅和场次信息
    if request.method == "POST":
        selected_room = request.POST.get("room")
        selected_session = request.POST.get("session")
    else:
        # 默认使用初始影厅和场次
        selected_room = movie_room1
        selected_session = movie_session1

    # 调用 showtimeSeat 函数
    totalSeat, emptySeat, picSave = showtimeSeat(
        theater1, movie_name1, movie_date1, selected_room, selected_session, pic_folder
    )
    seat_map_url = f"{settings.MEDIA_URL}{os.path.basename(picSave)}"

    # 将场次数据转换为字典列表格式
    session_data = m_sessions.to_dict(orient="records")

    context = {
        "current_date": movie_date1,
        "movie_poster_url": "https://capi.showtimes.com.tw/assets/60/6067b20f4ae07615325ac7026aa10d56.jpg",  # 電影url
        "seat_map_url": seat_map_url,
        "session_data": session_data,  # 场次数据
        "theater_name": theater1,
        "selected_room": selected_room,  # 当前选择的影厅
        "selected_session": selected_session,  # 当前选择的场次
    }

    return render(request, "ordering.html", context)
