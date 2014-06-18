from flask import json, request, make_response, redirect
from flask.ext.pushrod import pushrod_view
from bson import json_util
from datetime import date, datetime
from .utils import unixts
from .systemofrecord import SystemOfRecord
from .mint import Mint

from themint import app

db = SystemOfRecord(app.config)
mint = Mint(db)

@app.route('/titles', methods=['GET'])
@pushrod_view(jinja_template='titles.html')
def get():
    titles = {} # TODO ask systemofrecord
    body = json.dumps(list(titles), default=json_util.default)
    return {"titles" : json.loads(body) }

@app.route('/titles', methods=['POST'])
def post():
    payload = {}
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        payload = json.loads(request.form['payload'])
    else:
        payload = request.json # this has the payload, id, etc

    payload['created_ts'] = unixts()

    title = mint.create(payload)
    return redirect("/titles", code=302)
