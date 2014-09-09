from collections import OrderedDict
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto import Random
import json
import calendar
import datetime


def canonical_json(dictionary):
    def alphabetically_sorted_dict(d):
        ordered = OrderedDict()

        for k, v in sorted(d.items()):
            if isinstance(v, dict):
                ordered[k] = alphabetically_sorted_dict(v)
            else:
                ordered[k] = v
        return ordered

    return json.dumps(
        alphabetically_sorted_dict(dictionary),
        separators=(',', ':')
    )


def create_keys():
    random_generator = Random.new().read
    key = RSA.generate(1024, random_generator)
    return key.publickey().exportKey(), key


def sha256_sum(data):
    return SHA256.new(data).hexdigest()


def load_keys(public_file, private_file):
    key_file = open(public_file, "r")
    public_key = RSA.importKey(key_file)
    key_file.close()
    key_file = open(private_file, 'rb')
    private_key = RSA.importKey(key_file)
    key_file.close()

    return public_key, private_key


def unixts():
    return calendar.timegm(datetime.datetime.utcnow().timetuple())
