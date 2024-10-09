from search.models import movie,theater,showTimeInfo


def movieUpdate(data):
    title = data['電影名稱']
    img_src = data['電影海報網址']
    trailer_link=data['電影預告網址']
    movie_type=data["影片類型"]
    main_actor=data['主要演員']
    info = data['電影介紹']
    release_date = data['上或待上映']
    running_time = data['電影時長']
    screen_type = data['電影螢幕']
    if movie.objects.filter(title=title):
        return None
    movieData=movie.objects.create(title=title,img_src=img_src,trailer_link=trailer_link,\
                        movie_type=movie_type,main_actor=main_actor,info=info,release_date=release_date,\
                            running_time=running_time,screen_type=screen_type)
    movieData.save()
    
def theaterUpdate(data):
    name = data['戲院名稱']
    cinema=data['影城']
    address= data['影城位置']
    phone= data['影城電話']
    if theater.objects.filter(name=name):
        return None
    theaterData=theater.objects.create(name=name,cinema=cinema,address=address,phone=phone)
    theaterData.save()

def showUpdate(data):
    movieId=data['電影名稱']
    theaterId=data['影城']
    date=data['日期']
    time=data['時間']
    site=data['廳位席位']
    if movie.objects.filter(title=movieId) and theater.objects.filter(name=theaterId):
        movieId=movie.objects.get(title=movieId)
        theaterId=theater.objects.get(name=theaterId)
        showData=showTimeInfo.objects.create(movie=movieId,theater=theaterId,date=date,time=time,site=site)
        showData.save()

