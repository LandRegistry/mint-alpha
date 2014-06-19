import requests
import json

class SystemOfRecord(object):

    def __init__(self, config):
        endpoint = "/titles"
        self.api = config['SYSTEMOFRECORD_URL'] + endpoint

    def get(self, number=None):
        if number:
            response = requests.get(self.api + "/" + number)
            try:
                return json.dumps(response.json())
            except ValueError as e:
                return None
        else:
            # TODO get a collection of titles
            return {"not yet implemented" : 501}

    def put(self, signed_json_data):
        """payload requires sha256 and public key, although
        I'm currently not sure if validation should be done here."""

        headers = { "Content-Type" : "application/json"}
        data = json.dumps(signed_json_data)
        response = requests.post(self.api, data=data, headers=headers)
        return response
