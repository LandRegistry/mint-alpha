from themint import app
from themint.utils import unixts


class MintMessageService(object):
    def __init__(self, writer):
        self.writer = writer

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
        self.writer.send_to_system_of_record(signed)

    def health(self):
        return self.writer.health()
