import logging
from logging.handlers import RotatingFileHandler

from .utils import unixts
from themint import app


class Audit(object):
    def __init__(self):
        handler = RotatingFileHandler('audit.log', maxBytes=100000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    def log(self, message, status, **kwargs):
        stamp = unixts()
        app.logger.info('Audit start %s' % stamp)
        app.logger.info('Message: %s' % message)
        app.logger.info('Status code: %s' % status)

        for key, value in kwargs.iteritems():
            app.logger.info("%s = %s" % (key, value))

        app.logger.info('Audit end %s' % stamp)


