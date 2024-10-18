def submit_comment(request):
    if request.method == "POST":
        movie_name = request.POST.get("電影名稱")
        comment = request.POST.get("comment")
        movie = Movie.objects.filter(movie_name=movie_name).first()
        # 創建並保存評論
        review = Review(movie=movie, content=comment)
        review.save()
        return render(
            request, "comment_success.html", {"movie_name": movie_name}
        )  # 成功頁面


def a6(request):
    data = pd.read_csv("staticfiles/data3_utf8.csv", encoding="utf-8")

    cinema_groups = {}
    # 遍歷數據的每一行
    for index, row in data.iterrows():
        group_name = row["影城"]  # 影城名稱
        cinema_name = row["戲院"]  # 戲院名稱

        # 如果影城名稱不在字典中，則初始化
        if group_name not in cinema_groups:
            cinema_groups[group_name] = []

        # 將戲院名稱加入到相應的影城下
        cinema_groups[group_name].append(cinema_name)

    # 將字典轉換為列表格式，符合你的需求
    cinema_group_list = [
        {"group_name": group_name, "cinemas": cinemas}
        for group_name, cinemas in cinema_groups.items()
    ]
    if request.method == "GET":
        cinema = request.GET.get("cinema")
        selected_row = data[data["戲院"] == cinema]  # '戲院' 為你 CSV 中的列名
        tra = selected_row["交通方式"].iloc[0]
        sj = selected_row["介紹"].iloc[0]
        url = selected_row["戲院海報"].iloc[0]
        title = selected_row["戲院"].iloc[0]
    if request.method == "POST":
        cinema = request.POST.get("Select")  # 使用 POST 方法來獲取選擇的值
        selected_row = data[data["戲院"] == cinema]  # '戲院' 為你 CSV 中的列名
        tra = selected_row["交通方式"].iloc[0]
        sj = selected_row["介紹"].iloc[0]
        url = selected_row["戲院海報"].iloc[0]
        title = selected_row["戲院"].iloc[0]  # 取得該影院的交通方式
        return render(
            request,
            "6.html",
            {
                "cinema_groups": cinema_group_list,
                "tra": tra,
                "sj": sj,
                "url": url,
                "title": title,
            },
        )
    return render(
        request,
        "6.html",
        {
            "cinema_groups": cinema_group_list,
            "tra": tra,
            "sj": sj,
            "url": url,
            "title": title,
        },
    )
