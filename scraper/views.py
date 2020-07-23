from django.shortcuts import render

from django.http import HttpResponse
from . models import Scraper, Twitter, Country
from django.conf import settings
import os
from .apps import ScraperConfig
from scraper.forms import RouteForm
from django.views.generic import FormView
from django.core.mail import send_mail
from django.contrib import messages


#from django.views.generic import ListView

# scraping imports -------------------
from urllib.request import urlopen
from bs4 import BeautifulSoup
# -------------------------------

# twitter imports -----------------------------
import json
import requests
from requests_oauthlib import OAuth1
import gzip
#import dill
import re
#import joblib
# --------------------------------------------------


def scrape(request):

	country = request.POST.get('country') # getting the country abbreviation for javascript
	
	Scraper.objects.all().delete()
	Country.objects.all().delete()

	url = "https://www.newsnow.co.uk/h/World+News/Natural+Disasters"

	uClient = urlopen(url)
	page_html = uClient.read()
	uClient.close()
	page_soup = BeautifulSoup(page_html, 'html.parser')
	containers = page_soup.findAll('div', {'class':'newsfeed'})
	latest_news_container = containers[1].findAll('div', {'class': 'hl'})

	headlines = []
	links = []
	countries = []
	times = []

	for container in latest_news_container:
	    try:
	        headlines.append(container.a.text)
	    except:
	        headlines.append(None)
	        
	    try:
	        links.append(container.a['href'])
	    except:
	        links.append(None)
	        
	    try:
	        countries.append(container.span['c'])
	    except:
	        countries.append(None)
	        
	    try:
	        times.append(container.find('span', {'class':'time'}).text)
	    except:
	        times.append(None)

	# For individual country
	for i in range(len(headlines)):
		if country == countries[i]:
			Country.objects.create(Headlines = headlines[i], Links = links[i], Countries = countries[i], Date_Uploaded = times[i])
		
    	
    # General scraper ........
	for i in range(len(headlines)):
		Scraper.objects.create(Headlines = headlines[i], Links = links[i], Countries = countries[i], Date_Uploaded = times[i])


	results  = Scraper.objects.exclude(Countries = country)
	c_results = Country.objects.all()


	context = {'results':results,
	           'c_results':c_results,
	            'title':'Latest Information'}

	return render(request, 'scraper/scraped.html', context)


	# https://stackoverflow.com/questions/18598237/passing-variable-from-javascript-to-server-django



#class ScraperListView(ListView):
#	model = Scraper
#	template_name = "scraper/scraped.html"
#	context_object_name = 'results'
	#ordering = ['-Date_Uploaded']

# -----------------------------------------------------------------------------------------------------------------------------------

def tweet(request):
	Twitter.objects.all().delete()
	# Loading Twitter API secrets....
	api_path = os.path.join(settings.MODEL_API, 'twitter_secrets.json')
	with open(api_path, 'r') as f:
	    secrets = json.load(f)

	auth = OAuth1(secrets['api_key'],
	              secrets['api_secret_key'],
	              secrets['access_token'],
	              secrets['access_token_secret'])

	disaster_list = ['earthquake', 'flood', 'tornado', 'storm', 'wildfire','tsunami','hurricane','extreme heat', 'landslide','mudslide']


	url = 'https://api.twitter.com/1.1/search/tweets.json'
	count = 6   
	tweet_dict = {disaster: [] for disaster in disaster_list}

	for disaster in disaster_list:
	    params = {'q':disaster + ' -filter:retweets AND -filter:replies', 'lang':'en', 'count':count}

	    response = requests.get(url, auth=auth, params=params)
	    tweet_dict[disaster] += response.json()['statuses']
	    


	# Loading the Disaster Tweets model...
	for disaster in disaster_list:
	    for tweet in tweet_dict[disaster]:
	        if ScraperConfig.model.predict(ScraperConfig.text_prep.transform([tweet['text']])) == 0: 
	            tweet_dict[disaster].remove(tweet)


	tweets_info = []
	for disaster in disaster_list:
	    for tweet_json in tweet_dict[disaster]:
	        tweets_info.append({'tweet': tweet_json['text'],
	                    'day_created': tweet_json['created_at'],
	                    'username': tweet_json['user']['name'],
	                    'user_handle': tweet_json['user']['screen_name'],
	                    'location': tweet_json['user']['location']})

	tweets = []
	for ti in tweets_info:
	    tweets.append(ti['tweet'])

	bad_words = ['ass', 'fuck', 'fucking', 'bitch','dick','cunt','cunts','bitches','fuckers','whore','whores','pussy','dickhead','asshole','bastard']
	for i in range(len(tweets)):
	    clean_tweet = tweets[i].lower()
	    clean_tweet = re.sub(r"[!-()\"#/&@;:<>{}+=~|.?,]", "", clean_tweet)
	    for word in bad_words:
	        if word in clean_tweet.split():
	            del tweets_info[i]



	tweet =[]
	day_created =[]
	location =[]
	user_handle =[]
  
	for i in tweets_info:
		tweet.append(i['tweet'])
		day_created.append(i['day_created'])
		location.append(i['location'])
		user_handle.append(i['user_handle'])


	for i in range(len(tweet)):
		Twitter.objects.create(Tweets = tweet[i], Day_Created = day_created[i], Location = location[i], User_Handle = user_handle[i])


	infos  = Twitter.objects.all()


	context = {'infos': infos,
	           'title':' Twitter Information'}
	           
	return render(request, 'scraper/tweets.html', context)

# ---------------------------------------------------------------------------------------------------------------------------------

def map(request):
	if request.method == 'POST':
		Rform =  RouteForm(request.POST)
		if Rform.is_valid():
			pass
	else:
		Rform =  RouteForm()
   # -----------------------------------------------------------
	if request.method == 'POST':
		coor =  request.POST.get('location') #  request.POST['location']
		address = request.POST.get('address')  #  request.POST['address']
		subject ='Locate ME!'
		message =' I need help! I am at this address: {}, and these are my coordinates: {} if needed. A route to my current position can be gotten by pasting my address on the route engine on https://n-dia.herokuapp.com/scraper/maps/'.format(address, coor)
		email_from = settings.EMAIL_HOST_USER
		reciever = ['kenechiojukwu@gmail.com']
		send_mail(subject, message, email_from, reciever, fail_silently = False)
		messages.success(request, 'Your location has been successfully sent',extra_tags='alert')
		return redirect('scraper:maps') #/scraper/maps/
	

	return render(request,'scraper/maps.html', {'title': 'Maps','Rform': Rform})



    
	
	
	
		
		
	
