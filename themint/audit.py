from .utils import unixts
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from themint import app

class Audit(object):

    def __init__(self, config):
        # TODO proxy an audit service here. For now, just log to a file.
        handler = RotatingFileHandler('audit.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    def log(self, **kwargs):
        stamp = unixts()
        app.logger.info('Audit start %s' % stamp)
        for key, value in kwargs.iteritems():
            app.logger.info("%s = %s" % (key, value))
        app.logger.info('Audit end %s' % stamp)
