from flask import json, request, make_response, redirect
from flask.ext.pushrod import pushrod_view
from datetime import date, datetime
from .systemofrecord import SystemOfRecord
from .mint import Mint
from themint import app
from .audit import Audit

db = SystemOfRecord(app.config)
audit = Audit(app.config, db)
mint = Mint(db)

@app.route('/titles', methods=['GET'])
@app.route('/titles/<number>', methods=['GET'])
@pushrod_view(jinja_template='titles.html')
def get(number=None):
    titles = db.get(number)
    return {"titles" : [titles] }

@app.route('/titles', methods=['POST'])
def post():
    payload = {}
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        payload = json.loads(request.form['payload'])
    else:
        payload = request.json # this has the payload, id, etc

    r = mint.create(payload)

    audit.log(r.text, r.status_code, payload)

    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
        return redirect("/titles", code=302)
    else:
        return r.text, r.status_code
