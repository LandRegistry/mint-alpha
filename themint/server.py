from flask import json, request, make_response, redirect
from flask.ext.pushrod import pushrod_view
from datetime import date, datetime
from .mint import Mint
from themint import app

mint = Mint()


@app.route('/', methods=['GET'])
def index():
    return "Mint OK"

@app.route('/titles', methods=['POST'])
def post():
    payload = request.json
    mint.create(payload)
    # TODO the casework client will generate a unique title, which can be used to check the feeder for success
    return "Payload queued to system-of-record", 200
