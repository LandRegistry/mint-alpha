import os

class Config(object):
    DEBUG = False
    SYSTEMOFRECORD_URL = os.environ.get('SYSTEMOFRECORD_URL')
    REDIS_URL = os.environ.get('REDIS_URL')
    REDIS_NS_QUEUE_MINT = os.environ.get('REDIS_NS_QUEUE_MINT')

class DevelopmentConfig(Config):
    DEBUG = True

class TestConfig(DevelopmentConfig):
    TESTING = True
