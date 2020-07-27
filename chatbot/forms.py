from django import forms
from django.http import HttpResponse
from django.conf import settings
import os
import json

# Watson Dependencies
from ibm_watson import AssistantV2, ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


url = "https://api.us-south.assistant.watson.cloud.ibm.com/instances/20239426-5819-42dd-bc01-dd554723cf48"

ibm_path = os.path.join(settings.IBM_API, 'ibm_secrets.json')

with open(ibm_path , 'r') as f:
	secrets = json.load(f)
	    


class CommentForm(forms.Form):
	comment = forms.CharField(label='', widget = forms.Textarea(attrs={'class' : 'commentclass', 'placeholder':' e.g: Precautions to take during a flood?'})) # 'rows':4,'cols':90
                                                                               #'style':'width:650px; height: 60px; resize: none'

	def ask_watson(self):
		try:
		    authenticator = IAMAuthenticator(secrets['apikey'])
		    assistant = AssistantV2(
		        version=secrets['version'],
		        authenticator=authenticator
		    )
		    
		    assistant.set_service_url(url)
		    
		    sess_response = assistant.create_session(
		        assistant_id=secrets['assistant_id']
		    ).get_result()
		    
		    session_id = sess_response['session_id']
		    
		    response = assistant.message(
		        assistant_id=secrets['assistant_id'],
		        session_id=session_id,
		        input={
		            'message_type': 'text',
		            'text': self.cleaned_data['comment']
		        }
		    ).get_result()
		    
		    return(response['output']['generic'][0]['text'])
		    
		    sess_end_response = assistant.delete_session(
		    assistant_id=secrets['assistant_id'],
		    session_id=session_id
		    ).get_result()

		except ApiException as ex:
		    return('Method failed with status code' + str(ex.code) + ': ' + ex.message)
		    



# https://www.epilis.gr/en/blog/2016/08/18/ibm-watson-apis-django/
# https://stackoverflow.com/questions/5827590/css-styling-in-django-forms
# http://www.learningaboutelectronics.com/Articles/How-to-create-a-text-area-in-a-Django-form.php


class helpForm(forms.Form):
	place = forms.CharField(label='', max_length=3500, widget = forms.Textarea(attrs={'class' : 'placeclass','id':'id_place','placeholder':'Place of Occurence?'}))
	disaster_type = forms.CharField(label='', max_length=300, widget = forms.Textarea(attrs={'class' : 'typeclass','id':'id_disas','placeholder':'Disaster Type?'}))


class emailForm(forms.Form):
	email = forms.EmailField(label='', widget = forms.Textarea(attrs={'class' : 'emailclass','id':'id_email','placeholder':'sendmealerts@mail.com'}))
	#label='', max_length=3500, widget = forms.Textarea(attrs={'class' : 'emailclass','id':'id_email','placeholder':'sendmealerts@mail.com'})

   
   

