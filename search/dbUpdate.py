from search.models import movie,theater,showTimeInfo
from datetime import date

today=date.today()

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
    # 清除過期的電影(date__lt表示小於特定日期)
    showTimeInfo.objects.filter(date__lt=today).delete()

    # 加入新電影
    movieId=data['電影名稱']
    theaterId=data['影城']
    date=data['日期']
    time=data['時間']
    site=data['廳位席位']

    if movie.objects.filter(title=movieId) and theater.objects.filter(name=theaterId):
        movieId=movie.objects.get(title=movieId)
        theaterId=theater.objects.get(name=theaterId)
        if showTimeInfo.objects.filter(movie=movieId,theater=theaterId,date=date,time=time,site=site):
            return
        showData=showTimeInfo.objects.create(movie=movieId,theater=theaterId,date=date,time=time,site=site)
        showData.save()


if __name__=="__main__":
    data={'電影名稱':'test','影城':'test','日期':'2024-10-14','時間':'test','廳位席位':'test'}
    print(showUpdate(data))
