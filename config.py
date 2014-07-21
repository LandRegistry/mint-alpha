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

class DockerConfig(Config):
    DEBUG = True
    SYSTEMOFRECORD_URL = os.environ.get('SYSTEMOFRECORD_1_PORT_8000_TCP', '').replace('tcp://', 'http://')
    REDIS_URL = os.environ.get('REDIS_1_PORT_6379_TCP', '').replace('tcp://', 'http://')


