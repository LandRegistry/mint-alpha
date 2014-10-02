import cPickle as pickle
from redis import Redis

from themint import app


# TODO - add error handling

class SystemOfRecordWriteInterface(object):
    def __init__(self):
        self.redis = Redis.from_url(app.config.get('REDIS_URL'))
        self.ns = app.config.get('REDIS_NS_QUEUE_MINT')
        endpoint = "/titles"
        self.api = app.config.get('SYSTEMOFRECORD_URL') + endpoint

    def send_to_system_of_record(self, message):
        pickled = pickle.dumps(message)
        self.redis.rpush(self.ns, pickled)

    def health(self):
        try:
            self.redis.info()
            return True, "Redis"
        except Exception as e:
            app.logger.error("Exception in health check from redis: %s", repr(e))
            return False, "Redis"
