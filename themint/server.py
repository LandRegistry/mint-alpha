from flask import request, make_response
import json

from themint import app
from themint.service import mint_message_service


@app.route('/', methods=['GET'])
def index():
    return "Mint OK"


@app.route('/titles/<title_number>', methods=['POST'])
def post(title_number):
    app.logger.info("Received title number [%s] to mint new record with json: %s" % (title_number, request.json))
    mint_response = mint_message_service.wrap_message_for_system_of_record(request.json)
    app.logger.info("Response status code %s for title [%s]" % (mint_response.status_code, title_number))

    return make_response(
        json.dumps({
            'message': mint_response.text,
            'status_code': mint_response.status_code
        }),
        mint_response.status_code)
