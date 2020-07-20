from django.urls import path
from . import views
#from . views import ScraperListView


urlpatterns = [
    path('infomation/', views.scrape, name = 'scraper-scraped'),
    path('twitter_infomation/', views.tweet, name = 'scraper-tweets'),
    path('maps/', views.map, name = 'scraper-maps'),    
]