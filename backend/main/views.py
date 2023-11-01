from django.shortcuts import render
from .models import Travelogue, City

def index(request):
    travelogues = Travelogue.objects.all()[0:3]
    cities = City.objects.all()[0:8]
    return render(request, "main/index.html", {
        "travelogues": travelogues,
        "cities": cities,
        "page": "home"
    })

def travelogues(request):
    travelogues = Travelogue.objects.all()
    
    return render(request, "main/travelogues.html", {
        "travelogues": travelogues,
        "page": "travelogues"
        
    })

def travelogue(request, slug):
    travelogue = Travelogue.objects.get(slug=slug)

    return render(request, "main/travelogue.html", {
        "travelogue": travelogue,
    })

def places(request):
    cities = City.objects.all()

    return render(request, "main/places.html", {
        "cities": cities,
        "page": "places"
    })

def write(request):
    cities = City.objects.all()

    return render(request, "main/write.html", {
        "page": "write"
    })