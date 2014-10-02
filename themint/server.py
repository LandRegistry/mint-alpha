from flask import request, make_response
import json

from themint import app
from themint.service import message_service
from datatypes.core import str_to_uni_dict

@app.route('/', methods=['GET'])
def index():
    return "Mint OK"


@app.route('/titles/<title_number>', methods=['POST'])
def post(title_number):
    app.logger.info("Received title number [%s] to mint new record with json: %s" % (title_number, request.json))
    try:
        message_service.wrap_message_for_system_of_record(str_to_uni_dict(request.json))

        return make_response(
            json.dumps({
                'message': 'OK',
                'status_code': 201 
            }),
            201)
    except Exception as e:
        app.logger.error('Error when minting new: %s' % e)
        return make_response(
            json.dumps({
                'message': 'Error',
                'status_code': 400
            }),
            400)
