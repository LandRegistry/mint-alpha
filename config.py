import os

class DevelopmentConfig(object):
	SYSTEMOFRECORD_URL = os.environ.get('SYSTEMOFRECORD_URL', os.environ.get('SYSTEMOFRECORD_1_PORT_8001_TCP', '').replace('tcp://', 'http://'))
	DEBUG=True
