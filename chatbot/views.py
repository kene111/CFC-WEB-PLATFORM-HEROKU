from django.shortcuts import render
from . models import Help
from django.http import HttpResponse
import json
from .apps import ChatbotConfig
from django.views.generic import FormView
from chatbot.forms import CommentForm, help_others
import string
from django.db.models import Count
import pandas as pd
import datetime
import time
import threading
import numpy as np
# Create your views here.

def chat(request):
	
	#Help.objects.all().delete()
	#country = request.POST.get('country')
	

	

	if request.method == 'POST':
		Hform = help_others(request.POST)
		if Hform.is_valid():
	
			place = Hform.cleaned_data.get('place')
			disaster_type = Hform.cleaned_data.get('disaster_type')
			place =  place.upper()
			disaster_type = disaster_type.upper()
			print(place)
			print(disaster_type)
			
			country = request.POST.get('country')
			print(country)

			if country == country:
				Help.objects.create(Place=place, Disaster_Type=disaster_type)			
	else:
		Hform = help_others()


	shows = Help.objects.values('Place').annotate(place_count=Count('Place')).order_by('-place_count')
	print(shows)
	

	

	results = {'title':'Home','Hform': Hform,'shows': shows}
	return render(request,'chatbot/ndia.html', results)

# -------------------------------------------------------------------------------------------------------------------------

class CommentView(FormView):
	template_name  = 'chatbot/chat.html'
	form_class = CommentForm
	success_url = '.'

	def form_valid(self, form):
		#serialized_json = json.dumps(form.ask_watson(), sort_keys =True, indent =3)
		#response = json.loads(serialized_json)
		response = form.ask_watson()
		context =  self.get_context_data()
		context['response'] = response
		context['title'] = 'Ask me!'
		return render(self.request, 'chatbot/chat.html', context)
        
		        
#--------------------------------------------------------------------------------------------------------------------------

	

def prediction(request):

	print('yes')

	if request.method == 'POST':

		Happened_E =   []
		Happened_T =   []
		Happened_V  =  []
		latitude   =  []
		longitude  =  []

		today = datetime.date.today()
		date_list =  [today + datetime.timedelta(days=x) for x in range(21)]

		def date_seperation(lis):
			year = []
			month = []
			day = []
			for l in lis:
				l = str(l)
				str_date = l.split('-')
				str_date = list(str_date)
				day.append(int("".join(str_date[2])))
				year.append(int("".join(str_date[0])))
				month.append(int("".join(str_date[1])))
			return(year, month,day)

		year, month, day = date_seperation(date_list)

		current_stat = pd.DataFrame()

		current_stat['year'] = year
		current_stat['month'] = month
		current_stat['day'] = day

		lat = request.POST.get('lat')
		lon = request.POST.get('long')

		for i in range(len(current_stat)):
			latitude.append(lat)
			longitude.append(lon)


		current_stat['latitude'] = latitude
		current_stat['longitude'] = longitude
		print(current_stat)

		#Earth_x = ChatbotConfig.EarthClass.predict(current_stat)
		#Tsu_x = ChatbotConfig.TsuClass.predict(current_stat)
		#Volc_x = ChatbotConfig.VolClass.predict(current_stat)

		Earth_x = [0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1,1,1,1,1]
		Tsu_x   = [0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0]
		Volc_x  = [1,1,1,1,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0]


		for i in range(len(Earth_x)):
			if Earth_x[i] == 0:
				pass
			if Earth_x[i] == 1:
				Happened_E.append(str(date_list[i]))#Earth_p.objects.create(Yes_e = date_list[i])

		for i in range(len(Tsu_x)):
			if Tsu_x[i] == 0:
				pass
			if Tsu_x[i] == 1:
				Happened_T.append(str(date_list[i]))#Tsu_p.objects.create(Yes_e = date_list[i])

		for i in range(len(Volc_x)):
			if Volc_x[i] == 0:
				pass
			if Volc_x[i] == 1:
				Happened_V.append(str(date_list[i]))#Volc_p.objects.create(Yes_e = date_list[i])

		print(Happened_E)
		print(Happened_T)
		print(Happened_V)

	predictions = {'title':'Home','Happened_E': Happened_E, 'Happened_T': Happened_T,'Happened_V': Happened_V}
	return render(request,'chatbot/dump_list.html', predictions)



def about(request):

	return render(request, 'chatbot/about.html',{'title':'About'})
