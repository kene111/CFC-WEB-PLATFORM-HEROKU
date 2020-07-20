from django import forms
from django.http import HttpResponse
from django.conf import settings
import os
import json



class RouteForm(forms.Form):
	destination = forms.CharField(label='', max_length=300, widget = forms.Textarea(attrs={'class' : 'routeclass','id':'id_destination','placeholder':' Where do you want to go?'}))
   

