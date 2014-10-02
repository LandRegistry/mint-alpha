import os
from flask import Flask
import logging
from flask.ext.pushrod import Pushrod
from raven.contrib.flask import Sentry

from themint.service import system_of_record_write_interface

from themint.health import Health


app = Flask(__name__)
Pushrod(app)

app.config.from_object(os.environ.get('SETTINGS'))

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

if 'SENTRY_DSN' in os.environ:
    sentry = Sentry(app, dsn=os.environ['SENTRY_DSN'])

app.logger.info(app.config)

Health(app, checks=[system_of_record_write_interface.health])