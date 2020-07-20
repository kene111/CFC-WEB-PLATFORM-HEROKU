from django.contrib import admin
from . import models

# Register your models here.

mymodel = [models.Help]
admin.site.register(mymodel)   
