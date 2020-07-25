from django.shortcuts import render
#from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
	abbv= {"AF":"Afghanistan",
	"AX":"Aland Islands",
	"AL":"Albania",
	"DZ":"Algeria",
	"AS":"American Samoa",
	"AD":"Andorra",
	"AO":"Angola",
	"AI":"Anguilla",
	"AQ":"Antarctica",
	"AG":"Antigua and Barbuda",
	"AR":"Argentina",
	"AM":"Armenia",
	"AW":"Aruba",
	"AU":"Australia",
	"AT":"Austria",
	"AZ":"Azerbaijan",
	"BS":"Bahamas",
	"BH":"Bahrain",
	"BD":"Bangladesh",
	"BB":"Barbados",
	"BY":"Belarus",
	"BE":"Belgium",
	"BZ":"Belize",
	"BJ":"Benin",
	"BM":"Bermuda",
	"BT":"Bhutan",
	"BO":"Bolivia, Plurinational State of",
	"BQ":"Bonaire, Sint Eustatius and Saba",
	"BA":"Bosnia and Herzegovina",
	"BW":"Botswana",
	"BV":"Bouvet Island",
	"BR":"Brazil",
	"IO":"British Indian Ocean Territory",
	"BN":"Brunei Darussalam",
	"BG":"Bulgaria",
	"BF":"Burkina Faso",
	"BI":"Burundi",
	"KH":"Cambodia",
	"CM":"Cameroon",
	"CA":"Canada",
	"CV":"Cape Verde",
	"KY":"Cayman Islands",
	"CF":"Central African Republic",
	"TD":"Chad",
	"CL":"Chile",
	"CN":"China",
	"CX":"Christmas Island",
	"CC":"Cocos (Keeling) Islands",
	"CO":"Colombia",
	"KM":"Comoros",
	"CG":"Congo",
	"CD":"Congo, The Democratic Republic of the",
	"CK":"Cook Islands",
	"CR":"Costa Rica",
	"CI":"Côte d'Ivoire",
	"HR":"Croatia",
	"CU":"Cuba",
	"CW":"Curaçao",
	"CY":"Cyprus",
	"CZ":"Czech Republic",
	"DK":"Denmark",
	"DJ":"Djibouti",
	"DM":"Dominica",
	"DO":"Dominican Republic",
	"EC":"Ecuador",
	"EG":"Egypt",
	"SV":"El Salvador",
	"GQ":"Equatorial Guinea",
	"ER":"Eritrea",
	"EE":"Estonia",
	"ET":"Ethiopia",
	"FK":"Falkland Islands (Malvinas)",
	"FO":"Faroe Islands",
	"FJ":"Fiji",
	"FI":"Finland",
	"FR":"France",
	"GF":"French Guiana",
	"PF":"French Polynesia",
	"TF":"French Southern Territories",
	"GA":"Gabon",
	"GM":"Gambia",
	"GE":"Georgia",
	"DE":"Germany",
	"GH":"Ghana",
	"GI":"Gibraltar",
	"GR":"Greece",
	"GL":"Greenland",
	"GD":"Grenada",
	"GP":"Guadeloupe",
	"GU":"Guam",
	"GT":"Guatemala",
	"GG":"Guernsey",
	"GN":"Guinea",
	"GW":"Guinea-Bissau",
	"GY":"Guyana",
	"HT":"Haiti",
	"HM":"Heard Island and McDonald Islands",
	"VA":"Holy See (Vatican City State)",
	"HN":"Honduras",
	"HK":"Hong Kong",
	"HU":"Hungary",
	"IS":"Iceland",
	"IN":"India",
	"ID":"Indonesia",
	"IR":"Iran, Islamic Republic of",
	"IQ":"Iraq",
	"IE":"Ireland",
	"IM":"Isle of Man",
	"IL":"Israel",
	"IT":"Italy",
	"JM":"Jamaica",
	"JP":"Japan",
	"JE":"Jersey",
	"JO":"Jordan",
	"KZ":"Kazakhstan",
	"KE":"Kenya",
	"KI":"Kiribati",
	"KP":"Korea, Democratic People's Republic of",
	"KR":"Korea, Republic of",
	"KW":"Kuwait",
	"KG":"Kyrgyzstan",
	"LA":"Lao People's Democratic Republic",
	"LV":"Latvia",
	"LB":"Lebanon",
	"LS":"Lesotho",
	"LR":"Liberia",
	"LY":"Libya",
	"LI":"Liechtenstein",
	"LT":"Lithuania",
	"LU":"Luxembourg",
	"MO":"Macao",
	"MK":"Macedonia, Republic of",
	"MG":"Madagascar",
	"MW":"Malawi",
	"MY":"Malaysia",
	"MV":"Maldives",
	"ML":"Mali",
	"MT":"Malta",
	"MH":"Marshall Islands",
	"MQ":"Martinique",
	"MR":"Mauritania",
	"MU":"Mauritius",
	"YT":"Mayotte",
	"MX":"Mexico",
	"FM":"Micronesia, Federated States of",
	"MD":"Moldova, Republic of",
	"MC":"Monaco",
	"MN":"Mongolia",
	"ME":"Montenegro",
	"MS":"Montserrat",
	"MA":"Morocco",
	"MZ":"Mozambique",
	"MM":"Myanmar",
	"NA":"Namibia",
	"NR":"Nauru",
	"NP":"Nepal",
	"NL":"Netherlands",
	"NC":"New Caledonia",
	"NZ":"New Zealand",
	"NI":"Nicaragua",
	"NE":"Niger",
	"NG":"Nigeria",
	"NU":"Niue",
	"NF":"Norfolk Island",
	"MP":"Northern Mariana Islands",
	"NO":"Norway",
	"OM":"Oman",
	"PK":"Pakistan",
	"PW":"Palau",
	"PS":"Palestinian Territory, Occupied",
	"PA":"Panama",
	"PG":"Papua New Guinea",
	"PY":"Paraguay",
	"PE":"Peru",
	"PH":"Philippines",
	"PN":"Pitcairn",
	"PL":"Poland",
	"PT":"Portugal",
	"PR":"Puerto Rico",
	"QA":"Qatar",
	"RE":"Réunion",
	"RO":"Romania",
	"RU":"Russian Federation",
	"RW":"Rwanda",
	"BL":"Saint Barthélemy",
	"SH":"Saint Helena, Ascension and Tristan da Cunha",
	"KN":"Saint Kitts and Nevis",
	"LC":"Saint Lucia",
	"MF":"Saint Martin (French part)",
	"PM":"Saint Pierre and Miquelon",
	"VC":"Saint Vincent and the Grenadines",
	"WS":"Samoa",
	"SM":"San Marino",
	"ST":"Sao Tome and Principe",
	"SA":"Saudi Arabia",
	"SN":"Senegal",
	"RS":"Serbia",
	"SC":"Seychelles",
	"SL":"Sierra Leone",
	"SG":"Singapore",
	"SX":"Sint Maarten (Dutch part)",
	"SK":"Slovakia",
	"SI":"Slovenia",
	"SB":"Solomon Islands",
	"SO":"Somalia",
	"ZA":"South Africa",
	"GS":"South Georgia and the South Sandwich Islands",
	"ES":"Spain",
	"LK":"Sri Lanka",
	"SD":"Sudan",
	"SR":"Suriname",
	"SS":"South Sudan",
	"SJ":"Svalbard and Jan Mayen",
	"SZ":"Swaziland",
	"SE":"Sweden",
	"CH":"Switzerland",
	"SY":"Syrian Arab Republic",
	"TW":"Taiwan, Province of China",
	"TJ":"Tajikistan",
	"TZ":"Tanzania, United Republic of",
	"TH":"Thailand",
	"TL":"Timor-Leste",
	"TG":"Togo",
	"TK":"Tokelau",
	"TO":"Tonga",
	"TT":"Trinidad and Tobago",
	"TN":"Tunisia",
	"TR":"Turkey",
	"TM":"Turkmenistan",
	"TC":"Turks and Caicos Islands",
	"TV":"Tuvalu",
	"UG":"Uganda",
	"UA":"Ukraine",
	"AE":"United Arab Emirates",
	"UK":"United Kingdom",
	"US":"United States",
	"UM":"United States Minor Outlying Islands",
	"UY":"Uruguay",
	"UZ":"Uzbekistan",
	"VU":"Vanuatu",
	"VE":"Venezuela, Bolivarian Republic of",
	"VN":"Viet Nam",
	"VG":"Virgin Islands, British",
	"VI":"Virgin Islands, U.S.",
	"WF":"Wallis and Futuna",
	"EH":"Western Sahara",
	"YE":"Yemen",
	"ZM":"Zambia",
	"ZW":"Zimbabwe"}

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
			Country.objects.create(Headlines = headlines[i], Links = links[i], Countries = abbv[countries[i]], Date_Uploaded = times[i])
		
    	
    # General scraper ........
	for i in range(len(headlines)):
		Scraper.objects.create(Headlines = headlines[i], Links = links[i], Countries = abbv[countries[i]], Date_Uploaded = times[i])


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
	        if ScraperConfig.model.predict([tweet['text']]) == 0: #ScraperConfig.text_prep.transform()
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
		return redirect('scraper-maps') #/scraper/maps/
	

	return render(request,'scraper/maps.html', {'title': 'Maps','Rform': Rform})



    
	
	
	
		
		
	
