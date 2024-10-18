from django.db.models import Max
from .models import movie, theater, showTimeInfo
from .datafrom import miramar, ambassador, showtimes
from datetime import date
import pandas as pd

today = date.today()


def movieUpdate(datas):
    movie.objects.all().delete()
    moviesData = []
    movie_titles = [movie["title"] for movie in list(movie.objects.values("title"))]
    for data in datas:
        print(data["電影名稱"], "uploading...")
        ### 剛好遇到神奇字元所以replace...
        title = data["電影名稱"].replace("／", "/")
        img_src = data["電影海報網址"][:100]
        trailer_link = data["電影預告網址"][:100]
        movie_type = data["影片類型"][:100]
        main_actor = data["主要演員"][:100]
        info = data["電影介紹"][:500]
        release_date = data["上或待上映"][:100]
        running_time = data["電影時長"][:100]
        screen_type = data["電影螢幕"][:100]
        if title in movie_titles or title in [movie.title for movie in moviesData]:
            print(title, "already existed.")
            continue
        moviesData.append(
            movie(
                title=title,
                img_src=img_src,
                trailer_link=trailer_link,
                movie_type=movie_type,
                main_actor=main_actor,
                info=info,
                release_date=release_date,
                running_time=running_time,
                screen_type=screen_type,
            )
        )

    movie.objects.bulk_create(moviesData)


def theaterUpdate(datas):
    theatersData = []
    theater_name = [theater["name"] for theater in list(theater.objects.values("name"))]
    for data in datas:
        name = data["戲院名稱"][:100]
        cinema = data["影城"][:100]
        address = data["影城位置"][:100]
        phone = data["影城電話"][:100]
        if name in theater_name or name in [theater.name for theater in theatersData]:
            continue
        theatersData.append(
            theater(name=name, cinema=cinema, address=address, phone=phone)
        )

    theater.objects.bulk_create(theatersData)


def showUpdate(datas,is_limit=False):
    # 清除電影(date__lt表示小於特定日期)
    showTimeInfo.objects.filter(date__lt=today).delete()
    movies = movie.objects.all()
    theaters = theater.objects.all()
    showDatas = []

    for i, data in enumerate(datas):
        if is_limit and i > 500:
            break
        # 加入新電影
        print(data, "Running...")
        movieId = data["電影名稱"]
        theaterId = data["影城"]
        date = data["日期"][:100]
        time = data["時間"][:100]
        site = data["廳位席位"][:100]
        try:
            print(movieId)
            movieId = movies.get(title=movieId)
            theaterId = theaters.get(name=theaterId)
            show_data = showTimeInfo(
                movie=movieId, theater=theaterId, date=date, time=time, site=site
            )
            if show_data in showDatas:
                continue
            showDatas.append(show_data)
        except Exception as e:
            print(movieId, "error!", str(e))
            continue

    print("預計上傳筆數: ", len(showDatas))
    showTimeInfo.objects.bulk_create(showDatas)


### 下方為與爬蟲功能連結


def UpdateMovies():

    ### 秀泰
    sho_movies = showtimes.scrape_all_movies()

    ### 美麗華
    mir_movie = miramar.get_movie()
    # mir_show=miramar.get_showTimeInfo()

    ### 國賓
    amb_movie, amb_show = ambassador.get_movie_and_show()

    movies = pd.concat([mir_movie, amb_movie]).drop_duplicates(subset=["電影名稱"])
    movieUpdate(movies.to_dict("records"))
    # showUpdate(mir_show+mir_show)

    return {"result": "finish!"}


def UpdateShows():
    old_datas = pd.DataFrame(showTimeInfo.objects.all(), columns=["title"])
    old_datas["電影名稱"] = old_datas["title"].map(lambda x: str(x.movie))
    old_datas["影城"] = old_datas["title"].map(lambda x: str(x.theater))
    old_datas["日期"] = old_datas["title"].map(lambda x: str(x.date))
    # old_datas['時間']=old_datas['title'].map(lambda x: x.time)
    # old_datas['廳位席位']=old_datas['title'].map(lambda x: x.site)
    old_datas = old_datas.drop(columns=["title"])
    print(old_datas)

    ### datas
    ### 美麗華
    mir_show = miramar.get_showTimeInfo()

    ### 國賓
    amb_movie, amb_show = ambassador.get_movie_and_show()

    shows = pd.concat([mir_show, amb_show]).drop_duplicates()
    shows_unique = shows[
        ~shows[["電影名稱", "影城", "日期"]]
        .apply(tuple, axis=1)
        .isin(old_datas.apply(tuple, axis=1))
    ]
    print(shows_unique)

    showUpdate(shows_unique.to_dict("records"))
    return {"result": "finish!"}


def UpdateTheater(mode=''):
    ### 秀泰
    df=showtimes.scrape_cinema_info()
    datas = df.to_dict("records")
    theaterUpdate(datas)

    ### 美麗華
    df = miramar.get_theater()
    datas = df.to_dict("records")
    theaterUpdate(datas)

    ### 國賓
    df = ambassador.get_theater()
    datas = df.to_dict("records")
    theaterUpdate(datas)

    return {"result": "finish!"}


if __name__ == "__main__":
    df = showtimes.scrape_all_movies()
    df = pd.concat(df, mir_movie=miramar.get_movie())
    amb_movie, amb_show = ambassador.get_movie_and_show()
    df = pd.concat(df, amb_movie)
    df = df.drop_duplicates(subset=["電影名稱"])
