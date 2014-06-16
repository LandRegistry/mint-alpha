from Crypto.Hash import SHA256
from .utils import load_keys, create_keys


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
        #get current one from db using title_idenfier from incoming json
        #add link between incoming and current and then
        # hash and sign contents of incoming and save
        pass




