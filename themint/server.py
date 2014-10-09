from flask import request, make_response
import json

from themint import app
from themint.service import message_service

from datatypes.exceptions import DataDoesNotMatchSchemaException

@app.route('/', methods=['GET'])
def index():
    return "Mint OK"


# TODO remove <title_number> below, as it is not used.
@app.route('/titles/<title_number>', methods=['POST'])
def post(title_number):
    try:
        message_service.wrap_message_for_system_of_record(request.json)

        app.logger.info("Minting new title with payload %s" % (request.json))
        return make_response(
            json.dumps({
                'message': 'OK',
                'status_code': 201
            }),
            201)

    except DataDoesNotMatchSchemaException as e:
        app.logger.error('Validation error with data sent to mint %s' % e.field_errors)
        return make_response(
            json.dumps({
                'error': e.field_errors
            }), 400)

    except Exception as e:
        app.logger.error('Error when minting new', exc_info=e)
        return make_response(
            json.dumps({
                'message': 'Error',
                'status_code': 400
            }),
            400)
