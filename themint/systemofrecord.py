import requests

class SystemOfRecord(object):

    def __init__(self, config):
        self.systemofrecord_url = config['SYSTEMOFRECORD_URL']

    def put(self, signed_json_data):
        """payload requires sha256 and public key, although
        I'm currently not sure if validation should be done here."""
        r = requests.post(self.systemofrecord_url, data=signed_json_data)
        return r.status_code
