from django.apps import AppConfig
from django.conf import settings
import os
import dill



class ChatbotConfig(AppConfig):
    name = 'chatbot'

    Tsumodel_p = os.path.join(settings.ML_MODELS, 'tsu_classification_Model.dill')
    dill._dill._reverse_typemap['ClassType'] = type # Had to add this to stop a strange error from modern dill packages

    with open(Tsumodel_p, 'rb') as f:
        TsuClass = dill.load(f)



    earthquake_p = os.path.join(settings.ML_MODELS, 'earthquake_classification_model.dill')
    dill._dill._reverse_typemap['ClassType'] = type # Had to add this to stop a strange error from modern dill packages

    with open(earthquake_p, 'rb') as f:
        EarthClass = dill.load(f)



    volcano_p = os.path.join(settings.ML_MODELS, 'volcano_classification_model.dill')
    dill._dill._reverse_typemap['ClassType'] = type # Had to add this to stop a strange error from modern dill packages

    with open(volcano_p, 'rb') as f:
        VolClass = dill.load(f)


