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
    r = mint.create(payload)
    return r.text, r.status_code
