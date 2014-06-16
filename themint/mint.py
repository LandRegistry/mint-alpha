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
        return self.private_key.sign(hash,'')

    def __verify(self, original_data, signed):
        original_hashed = SHA256.new(original_data).hexdigest()
        return self.public_key.verify(original_hashed, signed)

    def create_entry(self, new_entry_json):
        # get current title from DB using title ID from incoming json
        print "Entry.id in create_entry"
        print new_entry_json['id']
        current_entry = self.db.db.entries.find_one({"id": new_entry_json['id']})

        # add link between incoming and current and then
        if current_entry:
            current_entry_hash = current_entry['md5sum']
            new_entry_json['previous'] = current_entry_hash

        # hash and sign contents of incoming and save
        new_entry_json['md5sum'] = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(16))
        self.db.db.entries.save(new_entry_json)
        new_entry_json
