import cPickle as pickle
from redis import Redis
import os
import json
import requests

from themint import app


# TODO - add error handling

class SystemOfRecordWriteInterface(object):
    def __init__(self):
        self.redis = Redis.from_url(app.config.get('REDIS_URL'))
        self.ns = app.config.get('REDIS_NS_QUEUE_MINT')
        endpoint = "/titles"
        self.api = app.config.get('SYSTEMOFRECORD_URL') + endpoint

    def send_to_system_of_record(self, message):
        if 'USE_QUEUE' in os.environ:
            pickled = pickle.dumps(message)
            self.redis.rpush(self.ns, pickled)
            return None
        else:
            headers = {"Content-Type": "application/json"}
            data = json.dumps(message)
            title_url = '%s/%s' % (self.api, message['title_number'])
            app.logger.info("Posting data %s to system or record at %s" % (data, title_url))
            response = requests.put(title_url, data=data, headers=headers)
            return response

    def health(self):
        try:
            self.redis.info()
            return True, "Redis"
        except Exception as e:
            app.logger.error("Exception in health check from redis: %s", repr(e))
            return False, "Redis"
