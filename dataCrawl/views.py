from django.shortcuts import render
from django.http import JsonResponse
from . import dbUpdate

# Create your views here.
    
def test(request):
    dbUpdate.UpdateMovies()
    dbUpdate.UpdateTheater()
    return render(request,"search/searchTest.html")