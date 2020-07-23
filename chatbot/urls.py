from django.urls import path
from . import views
from . views import CommentView

urlpatterns = [
    path('ndia/', views.chat, name = 'chatbot-ndia'), #ndia/
    path('chat/', CommentView.as_view(), name = 'chatbot-chat'),
    path('prediction/',  views.prediction, name = 'chatbot-prediction'),
     path('about/',  views.about, name = 'chatbot-about'),

]  