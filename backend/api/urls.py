from django.urls import path
from .views import *

urlpatterns = [
    path('api/register/', register, name='register'),
    path('api/login/', user_login, name='login'),
    path('api/travelogue/', travelogue_api, name='travelogue'),
    path('api/article/', article_api, name='article'),

]
