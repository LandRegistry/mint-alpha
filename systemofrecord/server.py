from flask import json, request, make_response
from bson import json_util
from datetime import datetime

from .mint import Mint

from systemofrecord import app, mongo

mint = Mint(mongo)

@app.route('/entries', methods=['GET','POST'])
def entries():
    if request.method == 'GET':
          db_entries = mongo.db.entries.find()
          return json.dumps(list(db_entries), default=json_util.default)
    else:
        created = request.json['created_date']
        #quick hack for date nonsense
        request.json['created_date'] =  datetime.strptime(created, "%Y-%m-%d")
        entry = mint.create_entry(request.json)
        return "200"
