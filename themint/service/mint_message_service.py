from themint import app
from themint.utils import unixts
from datatypes import system_of_record_request_validator
from datatypes.core import unicoded
import base64

class MintMessageService(object):
    def __init__(self, writer):
        self.writer = writer

    def wrap_message_for_system_of_record(self, message):
        signed = unicoded({
            'object' : {
                "data": base64.b64encode(message),
                "object_id": message['title_number'],
                "initial_request_timestamp": unixts()
                # optional:
                # created_by
                # reason_for_change
                # chains  [ chain_name, chain_value ]
            }
        })

        system_of_record_request_validator.validate(signed)

        app.logger.info("Submitting %s to the system or record" % signed)
        self.writer.send_to_system_of_record(signed)

    def health(self):
        return self.writer.health()
