from Crypto.Hash import SHA256
from .utils import load_keys, create_keys
import string
import random

class Mint(object):

    def __init__(self, db, public_key = None, private_key = None):
        self.db = db
        if public_key and private_key:
            self.public_key, self.private_key = load_keys(public_key, private_key)
        else:
            self.public_key, self.private_key = create_keys()

    def __sign(self, hash, key):
        # TODO implement signing
        # return self.private_key.sign(hash,'')
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))

    def __verify(self, original_data, signed):
        original_hashed = SHA256.new(original_data).hexdigest()
        return self.public_key.verify(original_hashed, signed)

    def create(self, json_data, previous_hash=None):
        """Signs a payload, then posts it to systemofrecord."""

        # reference to previous hash, if it exists
        if previous_hash:
            json_data['previous_sha256'] = previous_hash

        # sign the payload
        signed = self.__sign(json_data, None)
        json_data['sha256'] = signed
        return self.db.put(json_data)

        return new_json
