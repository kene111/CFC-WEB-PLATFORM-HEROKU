from django.contrib import admin

# Register your models here.
from .import models #import Scraper, Twitter

# Register your models here.
mymodels = [models.Scraper, models.Twitter, models.Country]
admin.site.register(mymodels)   