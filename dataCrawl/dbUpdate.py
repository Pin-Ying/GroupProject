from search.models import movie,theater,showTimeInfo
from .datafrom import miramar,ambassador
from datetime import date

today=date.today()

def movieUpdate(datas):
    moviesData=[]
    movie_titles=[movie['title'] for movie in list(movie.objects.values('title'))]
    for data in datas:
        title = data['電影名稱']
        img_src = data['電影海報網址'][:100]
        trailer_link=data['電影預告網址'][:100]
        movie_type=data["影片類型"][:100]
        main_actor=data['主要演員'][:100]
        info = data['電影介紹'][:500]
        release_date = data['上或待上映'][:100]
        running_time = data['電影時長'][:100]
        screen_type = data['電影螢幕'][:100]
        if title in movie_titles or title in [movie.title for movie in moviesData]:
            continue
        moviesData.append(movie(title=title,img_src=img_src,trailer_link=trailer_link,\
                            movie_type=movie_type,main_actor=main_actor,info=info,release_date=release_date,\
                                running_time=running_time,screen_type=screen_type))
        
    movie.objects.bulk_create(moviesData)
    
def theaterUpdate(datas):
    theatersData=[]
    theater_name=[theater['name'] for theater in list(theater.objects.values('name'))]
    for data in datas:
        name = data['戲院名稱'][:100]
        cinema = data['影城'][:100]
        address= data['影城位置'][:100]
        phone= data['影城電話'][:100]
        if name in theater_name or name in [theater.name for theater in theatersData]:
            continue
        theatersData.append(theater(name=name,cinema=cinema,address=address,phone=phone))
    
    theater.objects.bulk_create(theatersData)

def showUpdate(datas):
    # 清除過期的電影(date__lt表示小於特定日期)
    showTimeInfo.objects.filter(date__lt=today).delete()
    
    showsData=[]
    movies=movie.objects.all()
    theaters=theater.objects.all()

    for data in datas:
    # 加入新電影
        movieId=data['電影名稱']
        theaterId=data['影城']
        date=data['日期'][:100]
        time=data['時間'][:100]
        site=data['廳位席位'][:100]

        if movies.filter(title=movieId) and theaters.filter(name=theaterId):
            movieId=movie.objects.get(title=movieId)
            theaterId=theater.objects.get(name=theaterId)
            if showTimeInfo(movie=movieId,theater=theaterId,date=date,time=time,site=site) in showsData:
                continue
            showsData.append(showTimeInfo(movie=movieId,theater=theaterId,date=date,time=time,site=site))

    showTimeInfo.objects.bulk_create(showsData)


### 下方為與爬蟲功能連結

def UpdateMovies():
    ### datas
    ### 美麗華
    mir_movie=miramar.get_movie()
    # mir_show=miramar.get_showTimeInfo()

    ### 國賓
    amb_movie,amb_show=[data.to_dict("records") for data in ambassador.get_movie_and_show()]
    movieUpdate(mir_movie+amb_movie)
    # showUpdate(mir_show+mir_show)

    return {"result": "finish!"}

def UpdateShows():
    ### datas
    ### 美麗華
    # mir_movie=miramar.get_movie()
    mir_show=miramar.get_showTimeInfo()

    ### 國賓
    amb_movie,amb_show=[data.to_dict("records") for data in ambassador.get_movie_and_show()]
    # movieUpdate(mir_movie+amb_movie)
    showUpdate(mir_show+mir_show)

    return {"result": "finish!"}

def UpdateTheater():
    ### 美麗華
    df=miramar.get_theater()
    datas=df.to_dict("records")
    theaterUpdate(datas)
    
    ### 國賓
    df=ambassador.get_theater()
    datas=df.to_dict("records")
    theaterUpdate(datas)

    return {"result": "finish!"}

