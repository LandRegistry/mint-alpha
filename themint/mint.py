from Crypto.Hash import SHA256
from datadiff import diff
from .utils import load_keys, create_keys, sha256_sum, unixts
import string
import random
import json

class Mint(object):

    def __init__(self, db, public_key = None, private_key = None):
        self.db = db
        if public_key and private_key:
            self.public_key, self.private_key = load_keys(public_key, private_key)
        else:
            self.public_key, self.private_key = create_keys()

    def __sign(self, clear_text, key=None):
        # TODO implement signing
        if not key:
            key = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
        cipher_text = self.private_key.sign(clear_text,key)
        return cipher_text

    def __verify(self, original_data, signed):
        original_hashed = SHA256.new(original_data).hexdigest()
        return self.public_key.verify(original_hashed, signed)

    def diff_with_previous(self, json_data):
        """
        Accept JSON data; extract the title_number;
        Get the last known version for said title_number;
        Post to systemofrecord.
        Create datadiff between old and new version.
        Send datadiff + response status code + response status message
        to the audit service.
        (my suggestion for  audit log messages is to just drop them onto
        a queue for now).
        """
        title_number = json_data['title_number']
        doc = self.db.get(title_number)
        if doc:
            previous_json = json.loads(doc)
            title = previous_json['title']
            print "DIFF"
            print diff(title, json_data)
        else:
            print "NO PREVIOUS VERSION FOR %s" % title_number
        # TODO finish this
        pass

    def create(self, json_data, previous_hash=None):
        """Signs a payload, then posts it to systemofrecord."""

        # reference to previous hash, if it exists
        if previous_hash:
            json_data['previous_sha256'] = previous_hash

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
        return self.db.put(signed)
