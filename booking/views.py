from django.shortcuts import render

# Create your views here.

def booking_index(request):
    return render(request,"booking_form.html")
