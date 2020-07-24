from django.db import models

# Create your models here.

#from django.utils import timezone

# Create your models here.

class Scraper(models.Model):
	Headlines = models.CharField(max_length=3000)
	Links = models.TextField(default="")
	Countries = models.CharField(max_length=60, default="")
	Date_Uploaded = models.TextField(default="")

	def __str__(self):
		return self.Headlines

	#class Meta:
	#	abstract =True


class Country(Scraper):
	pass
	

	 
	def __str__(self):
		return self.Headlines
	

    
	

class Twitter(models.Model):
	Tweets = models.TextField(default="")
	Day_Created = models.TextField(default="")
	Location = models.CharField(max_length =50, default="")
	User_Handle = models.CharField(max_length=90, default="")


	def __str__(self):
		return self.Tweets   

	
    
