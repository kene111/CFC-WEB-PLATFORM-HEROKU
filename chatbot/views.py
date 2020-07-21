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
from  django.db.models import Max
import pytz
# Create your views here.

def chat(request):


	country = request.POST.get('country')

	shows = []
	

	if request.method == 'POST':
		Hform = help_others(request.POST)
		if Hform.is_valid():
	
			place = Hform.cleaned_data.get('place')
			disaster_type = Hform.cleaned_data.get('disaster_type')
			place =  place.upper()
			disaster_type = disaster_type.upper()
		
			if country == country:
				Help.objects.create(Place=place, Disaster_Type=disaster_type)



			print('error starts here')
			get_max = Help.objects.values_list('Place').annotate(place_count=Count('Place')).order_by('-place_count').first() #[0] # get the highest occuring variable in place column
			if get_max == None:
				pass
			else:
				max_var = get_max[0] # the variable, string.
				filt = Help.objects.filter(Place = max_var).aggregate(maxoccurance=Max('Disaster_Type'))['maxoccurance'] # filter by max occuring disaster type
				shows = Help.objects.filter(Place = max_var, Disaster_Type = filt)[0:1]

				now = datetime.datetime.now(tz=pytz.UTC)
				tnow = [now]

				def Time_Hour(time):
				    hour = []
				    for ti in time:
				        ti = str(ti)
				        h = ti.split(' ')
				        h = list(h)
				        hour.append(int("".join(h[1][0:2]))) 
				       
				    return(hour)

				value = Time_Hour(tnow)

				if value[0] == 24:
					Help.objects.all().delete() # clearing the database after 24 hrs

				results = {'title':'Home','Hform': Hform,'shows': shows}
				return render(request,'chatbot/ndia.html', results)

	else:
		Hform = help_others()

	results = {'title':'Home','Hform': Hform,'shows': shows}
	return render(request,'chatbot/ndia.html', results)

'''
	print('error starts here')
	get_max = Help.objects.values_list('Place').annotate(place_count=Count('Place')).order_by('-place_count').first()#[0] # get the highest occuring variable in place column
	if get_max == None:
		pass
	else:
		max_var = get_max[0] # the variable, string.
		filt = Help.objects.filter(Place = max_var).aggregate(maxoccurance=Max('Disaster_Type'))['maxoccurance'] # filter by max occuring disaster type
		print(filt)
		shows = Help.objects.filter(Place = max_var, Disaster_Type = filt)[0:1]
		print(shows)

		now = datetime.datetime.now(tz=pytz.UTC)
		tnow = [now]

		def Time_Hour(time):
		    hour = []
		    for ti in time:
		        ti = str(ti)
		        h = ti.split(' ')
		        h = list(h)
		        hour.append(int("".join(h[1][0:2]))) 
		       
		    return(hour)

		value = Time_Hour(tnow)

		if value[0]== 24:
			Help.objects.all().delete() # clearing the database after 24 hrs

	    
'''
	#results = {'title':'Home','Hform': Hform,'shows': shows}
	#return render(request,'chatbot/ndia.html', results)

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
		

		Earth_x = ChatbotConfig.EarthClass.predict(current_stat)
		Tsu_x = ChatbotConfig.TsuClass.predict(current_stat)
		Volc_x = ChatbotConfig.VolClass.predict(current_stat)

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

	predictions = {'title':'Home','Happened_E': Happened_E, 'Happened_T': Happened_T,'Happened_V': Happened_V}
	return render(request,'chatbot/dump_list.html', predictions)







def about(request):

	return render(request, 'chatbot/about.html',{'title':'About'})
