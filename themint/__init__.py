import os, sys
from flask import Flask
from flask.ext.basicauth import BasicAuth
from flask.ext.pushrod import Pushrod

app = Flask(__name__)
Pushrod(app)

# add config
app.config.from_object('config')
if app.config['SYSTEMOFRECORD_URL'] == '':
    print "Required environment variable not set: SYSTEMOFRECORD_URL"
    sys.exit(-1)

# auth
if os.environ.get('BASIC_AUTH_USERNAME'):
    app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
    app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)
