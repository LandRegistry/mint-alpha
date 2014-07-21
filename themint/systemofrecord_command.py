import cPickle as pickle
from redis import Redis, WatchError
from themint import app
import os
import json
import requests

#TODO - add error handling

class SystemOfRecordCommand(object):

    def __init__(self):
        self.redis = Redis.from_url(app.config.get('REDIS_URL'))
        self.ns = app.config.get('REDIS_NS_QUEUE_MINT')
        endpoint = "/titles"
        self.api = app.config.get('SYSTEMOFRECORD_URL') + endpoint

    def put(self, signed_json_data):
        """payload requires sha256 and public key, although
        I'm currently not sure if validation should be done here."""

        if 'USE_QUEUE' in os.environ:
            pickled = pickle.dumps(signed_json_data)
            self.redis.rpush(self.ns, pickled)
            return None
        else:
            headers = { "Content-Type" : "application/json"}
            data = json.dumps(signed_json_data)
            title_url = '%s/%s' % (self.api, signed_json_data['title_number'])
            app.logger.info("Posting data %s to system or record at %s" %(data, title_url))
            response = requests.put(title_url, data=data, headers=headers)
            return response
