import os, sys
from flask import Flask
import logging
from flask.ext.basicauth import BasicAuth
from flask.ext.pushrod import Pushrod

app = Flask(__name__)
Pushrod(app)

app.config.from_object(os.environ.get('SETTINGS'))

if not app.debug:
    app.logger.addHandler(logging.StreamHandler())
    app.logger.setLevel(logging.INFO)

app.logger.info( "============")
app.logger.info(app.config)
app.logger.debug(app.debug)
app.logger.info("============")

