from django.shortcuts import render
from search.models import movies
import re

# test 123456789

# Create your views here.


def search(request,methods=['GET','POST']):
    if request.method=='GET':
        return render(request,'search.html')

    search=request.POST
    searchDic={key:search[key] for key in search if search[key]!=""}
    # print(searchDic)

    datas=movies.objects.all()
    datas=[{'movieTitle':data.title,'movieScreen':data.screen,'area':data.area,'theater':data.theater} for data in datas]
    
    ### 搜尋欄無填寫視為全搜尋
    if len(searchDic)==1:
        results=datas
        return render(request,'search.html',locals())
    
    ### 針對螢幕篩選先重新建構字典
    screens=['Imax','3D','digital']
    searchDic['movieScreen']=[]
    for screen in screens:
        if screen in searchDic.keys():
            searchDic['movieScreen'].append(screen)
            searchDic.pop(screen)
    print(searchDic)

    try:
        results=[]
        ### 電影標題搜尋
        if 'movieTitle' in searchDic:
            for data in datas:
                results.append(data) if re.search(searchDic['movieTitle'], data['movieTitle']) else None
            datas=results

        results=[]
        ### 其他搜尋
        for data in datas:
            match=0
            for key in ["movieScreen","area","theater"]:
                match+=1 if key in searchDic and data[key] in searchDic[key] else 0
            results.append(data) if match!=0 else None
        datas=results if len(results)>0 else datas

    except Exception as e:
        print(e)
        datas=['error!']
    
    return render(request,'search.html',locals())