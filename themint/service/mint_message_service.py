from themint import app
from themint.audit import Audit
from themint.service import system_of_record_write_interface


class MintMessageService(object):
    def __init__(self):
        self.audit = Audit(app.config)

    def wrap_message_for_system_of_record(self, message):
        signed = {
            "title": message,
            "title_number": message['title_number'],
            "sha256": str(encrypted_sum[0]),
            "public_key": str(self.public_key),
            "created_ts": unixts()
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
