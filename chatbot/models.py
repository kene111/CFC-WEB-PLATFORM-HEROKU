from django.db import models

# Create your models here.

class Help(models.Model):
	Place = models.TextField(max_length=3000)
	Disaster_Type = models.CharField(default=" ", max_length=3000)

	def __str__(self):
		return self.Place


#class Earth_p(models.Model):
#	Yes_e =  models.TextField(max_length=300,default=None,null=True)

#	def __str__(self):
#		return self.Yes_e


#class Tsu_p(models.Model):
#	Yes_t =  models.TextField(max_length=300,default=None, null=True)

#	def __str__(self):
#		return self.Yes_t


#class Volc_p(models.Model):
#	Yes_v =  models.TextField(max_length=300,default=None,null=True)
	
#	def __str__(self):
#		return self.Yes_v