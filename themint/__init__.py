import os
from flask import Flask
from flask.ext.basicauth import BasicAuth
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

# add mongo config

# auth
if os.environ.get('BASIC_AUTH_USERNAME'):
    app.config['BASIC_AUTH_USERNAME'] = os.environ['BASIC_AUTH_USERNAME']
    app.config['BASIC_AUTH_PASSWORD'] = os.environ['BASIC_AUTH_PASSWORD']
    app.config['BASIC_AUTH_FORCE'] = True
    basic_auth = BasicAuth(app)


