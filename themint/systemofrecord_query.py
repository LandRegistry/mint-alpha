import json
import requests
from themint import app


class SystemOfRecordQuery(object):

    def __init__(self):
        endpoint = "/titles"
        self.api = app.config.get('SYSTEMOFRECORD_URL') + endpoint

    def get_title(self, title):
        response = requests.get(self.api + '/' + title)
        return response

    def get_last(self):
        response = requests.get(self.api + '/last')
        return response
        
