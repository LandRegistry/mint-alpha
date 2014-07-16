import os

class DevelopmentConfig(object):
    SYSTEMOFRECORD_URL = os.environ.get('SYSTEMOFRECORD_URL', os.environ.get('SYSTEMOFRECORD_1_PORT_8001_TCP', '').replace('tcp://', 'http://'))
    REDIS_URL = os.environ.get('REDIS_URL')
    REDIS_NS_MINT = os.environ.get('REDIS_NS_MINT')
    DEBUG=True
