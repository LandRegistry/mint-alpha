from themint import app
from themint.audit import Audit
from themint.service import system_of_record_write_interface
from themint.utils import unixts


class MintMessageService(object):
    def __init__(self):
        self.audit = Audit()

    def wrap_message_for_system_of_record(self, message):
        signed = {
            "data": message,
            "object_id": message['title_number'],
            "initial_request_timestamp": unixts()
            # optional:
            # created_by
            # reason_for_change
            # chains  [ chain_name, chain_value ]
        }

        app.logger.info("Submitting %s to the system or record" % signed)
        response = system_of_record_write_interface.send_to_system_of_record(signed)

        if not response:
            response = Response('Payload queued to system-of-record', 200)
        else:
            response = Response(response.text, response.status_code)

        app.logger.info("Response: %s" % response)
        self.audit.log(response.text, response.status_code, message)
        return response


class Response(object):
    def __init__(self, text, code):
        self.text = text
        self.status_code = code
