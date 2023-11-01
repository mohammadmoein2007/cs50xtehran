from django.urls import path
from .views import *

app_name = "main"

urlpatterns = [
    path('', index, name='index'),
    path('travelogues/', travelogues, name='travelogues'),
    path('places/', places, name='places'),
    path('travelogue/<slug:slug>', travelogue, name='travelogue'),
    path('write/', write, name='write'),


]
