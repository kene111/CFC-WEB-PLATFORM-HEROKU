from django.db import models

# Create your models here.

class Help(models.Model):
	Place = models.TextField(max_length=3000)
	Disaster_Type = models.CharField(default=" ", max_length=3000)

	def __str__(self):
		return self.Place

	class Meta:
		get_latest_by = ['Place']


class Emails(models.Model):
	Email =  models.EmailField(max_length=200,null=True,blank=True)

	def __str__(self):
		return self.Email

