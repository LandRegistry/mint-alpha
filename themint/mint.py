from Crypto.Hash import SHA256
from .utils import load_keys, create_keys, sha256_sum, unixts
import string
import random
from themint import app
from .audit import Audit
from .systemofrecord_command import SystemOfRecordCommand
from .systemofrecord_query import SystemOfRecordQuery


class Mint(object):
    """
    Talks to system-of-record by way of commands and queries.
    See http://martinfowler.com/bliki/CQRS.html
    """

    def __init__(self, public_key = None, private_key = None):
        self.command = SystemOfRecordCommand()
        self.query = SystemOfRecordQuery()
        self.audit = Audit(app.config)
        if public_key and private_key:
            self.public_key, self.private_key = load_keys(public_key, private_key)
        else:
            self.public_key, self.private_key = create_keys()

    def __sign(self, clear_text, key=None):
        if not key:
            key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
        cipher_text = self.private_key.sign(clear_text,key)
        return cipher_text

    def __verify(self, original_data, signed):
        original_hashed = SHA256.new(original_data).hexdigest()
        return self.public_key.verify(original_hashed, signed)


    def create(self, json_data, previous_hash=None):
        """Signs a payload, then posts it to systemofrecord."""

        # reference to previous hash, if it exists
        last = None
        if previous_hash:
            json_data['previous_sha256'] = previous_hash
        else:
            # get the sha256_hash of the previous entry
            last_resp = self.query.get_last()
            try:
                last = last_resp.json()
                json_data['previous_sha256'] = last['sha256']
            except ValueError:
                pass

        # TODO canonicalise the payload
        canonical_json = str(json_data)

        app.logger.info("Recieved the following json %s" % json_data)

        # sign the payload
        sha_sum = sha256_sum(canonical_json)

        # encrypt the sum
        encrypted_sum = self.__sign(sha_sum)
        signed = {
            "title" : json_data,
            "title_number" : json_data['title_number'],
            "sha256" : str(encrypted_sum[0]),
            "public_key" : str(self.public_key),
            "created_ts" : unixts()
        }

        app.logger.info("Submitting %s to the system or record" % signed)
        response = self.command.put(signed)

        # TODO gauranteed delivery? Response code?
        if not response:
            # TODO return a meaningful response, although this is fire and forget
            response = Response('Payload queued to system-of-record', 200)
        else:
            response = Response(response.text, response.status_code)

        app.logger.info( "Response: %s" % response)
        self.audit.log(response.text, response.status_code, json_data, last)
        return response


class Response(object):

    def __init__(self, text, code):
        self.text = text
        self.status_code = code
