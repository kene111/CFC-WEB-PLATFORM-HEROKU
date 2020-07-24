from django.apps import AppConfig
from django.conf import settings

import gzip
import dill
import os
#import pickle
#import joblib
#from sklearn.base import BaseEstimator, TransformerMixin
#import re
#from nltk.corpus import stopwords 
#from nltk.tokenize import word_tokenize


class ScraperConfig(AppConfig):
    name = 'scraper'

#   class TextPreprocessor(BaseEstimator, TransformerMixin):
#        def __init__(self):
#            pass
#        
#        def fit(self, X, y=None):
#            return self
#
#        @staticmethod
#        def clean_text(text):
#
#
#            stop_words = set(stopwords.words('english'))
#            stop_words.update(['thi', 'amp', 'wa', 'via', 'ha', 'us', 'will', 'new', "n't", 'like', '\n'])
#
#            text = text.lower()
#            text = re.sub(r"i'm", "i am", text)
#            text = re.sub(r"he's", "he is", text)
#            text = re.sub(r"she's", "she is", text)
#            text = re.sub(r"that's", "that is", text)
#            text = re.sub(r"what's", "what is", text)
#            text = re.sub(r"where's", "where is", text)
#            text = re.sub(r"\'ll", " will", text)
#            text = re.sub(r"\'ve", " have", text)
#            text = re.sub(r"\'re", " are", text)
#            text = re.sub(r"\'d", " would", text)
#            text = re.sub(r"won't", "will not", text)
#            text = re.sub(r"can't", "cannot", text)
#            text = re.sub(r"[-()\"#/&@;:<>{}+=~|.?,]", "", text)
#            text = re.sub(r"http\S+", "", text)
#            text = re.sub(r"https\S+", "", text)
#            text = re.sub(r"û", "", text)
#
#            word_tokens = word_tokenize(text) 
#            filtered_sentence = [w for w in word_tokens if not w in stop_words] 
#            filtered_sentence = [] 
#
#            for w in word_tokens: 
#                if w not in stop_words: 
#                    filtered_sentence.append(w) 
#
#            return ' '.join(filtered_sentence)
#
#        def transform(self, X):
#            clean_X = []
#            for text in X:
#                clean_X.append(self.clean_text(text))
#                
#            return clean_X
#
#    
#    text_prep = TextPreprocessor()
#    
#
    model_path = os.path.join(settings.MODEL_API, 'natural_disaster_text_model.dill')
    dill._dill._reverse_typemap['ClassType'] = type # Had to add this to stop a strange error from modern dill packages

    with open(model_path, 'rb') as f:
        model = dill.load(f)     

