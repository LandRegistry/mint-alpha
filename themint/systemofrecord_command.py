import cPickle as pickle
from redis import Redis, WatchError
from themint import app

class SystemOfRecordCommand(object):

    def __init__(self):
        self.redis = Redis.from_url(app.config.get('REDIS_URL'))
        self.ns = app.config.get('REDIS_NS_MINT')

    def put(self, signed_json_data):
        """payload requires sha256 and public key, although
        I'm currently not sure if validation should be done here."""

        pickled = pickle.dumps(signed_json_data)
        self.redis.set(self.ns, pickled)
