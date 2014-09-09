import logging
from logging.handlers import RotatingFileHandler
from datadiff import diff

from .utils import unixts
from themint import app


class Audit(object):
    def __init__(self, config):
        # TODO proxy an audit service here. For now, just log to a file.
        handler = RotatingFileHandler('audit.log', maxBytes=10000, backupCount=1)
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    def log(self, message, status, json_data, last, **kwargs):
        stamp = unixts()
        app.logger.info('Audit start %s' % stamp)
        app.logger.info('Message: %s' % message)
        app.logger.info('Status code: %s' % status)

        # TODO diff doesn't make sense for how systemofrecord currently works,
        # because 'last' isn't necessarily related to the current title.
        # difference = self.__diff(json_data, last)
        #        if difference:
        #            app.logger.info('Diff: \n%s' % difference)
        for key, value in kwargs.iteritems():
            app.logger.info("%s = %s" % (key, value))
        app.logger.info('Audit end %s' % stamp)

    def __diff(self, json_data, last):
        """
        Diff the new JSON data with the last version,
        and return a textual representation of it.
        """
        title_number = json_data['title_number']
        if last:
            last_title = last['title']
            difference = diff(last_title, json_data)
            return str(difference)
        else:
            return None
