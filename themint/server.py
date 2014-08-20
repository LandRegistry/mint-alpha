from flask import request, make_response
from .mint import Mint
from themint import app
from .health import Health
import json

mint = Mint()
Health(app, checks=[mint.health])


@app.route('/', methods=['GET'])
def index():
    return "Mint OK"


@app.route('/titles/<title_number>', methods=['POST'])
def post(title_number):
    app.logger.info(
            "Recieved title number %s to mint new record with json %s" %
            (title_number, request.json))
    r = mint.create(request.json)
    app.logger.info("Response status code %s" % r.status_code)
    return make_response(
            json.dumps({
                'message': r.text,
                'status_code': r.status_code}),
            r.status_code)
