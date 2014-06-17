from flask import json, request, make_response
from flask.ext.pushrod import pushrod_view
from bson import json_util
from datetime import date, datetime

from .mint import Mint

from themint import app, mongo

mint = Mint(mongo)

@app.route('/entries', methods=['GET'])
@pushrod_view(jinja_template='entry.html')
def get_entries():
    entries = mongo.db.entries.find()
    body = json.dumps(list(entries), default=json_util.default)
    return {"entries" : json.loads(body) }

@app.route('/entries', methods=['POST'])
def create_entries():
    payload = {}
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        pl = request.form['payload']
        print "PAYLOAD"
        print pl
        payload = json.loads(request.form['payload'])
    else:
        # request.json['created_date'] =  date.today()
        payload = request.json # this has the payload, id, etc

    payload['created_date'] = str(date.today())

    entry = mint.create_entry(payload)
    return "200"
