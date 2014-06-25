from Crypto.Hash import SHA256
from .utils import load_keys, create_keys, sha256_sum, unixts
import string
import random
import json
from themint import app
from .audit import Audit

class Mint(object):

    def __init__(self, db, public_key = None, private_key = None):
        self.db = db
        self.audit = Audit(app.config, db)
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
            last_resp = self.db.get()
            try:
                last = last_resp.json()
                json_data['previous_sha256'] = last['sha256']
            except ValueError:
                pass

        # TODO canonicalise the payload
        canonical_json = str(json_data)

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
        resp = self.db.put(signed)

        self.audit.log(resp.text, resp.status_code, json_data, last)

        return resp
