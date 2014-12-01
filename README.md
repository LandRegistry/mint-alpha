# Mint

[![Build Status](https://travis-ci.org/LandRegistry/mint.svg)](https://travis-ci.org/LandRegistry/mint)

[![Coverage Status](https://img.shields.io/coveralls/LandRegistry/mint.svg)](https://coveralls.io/r/LandRegistry/mint)

# What?

Service to create new versions of a title, hashed and signed.

Takes a document in this form:

https://raw.githubusercontent.com/LandRegistry/migration-emitter/master/samples/BD161871.json

...before posting it to the [System Of Record](https://github.com/landregistry/system-of-record).


#Dependencies:

- System of record service - https://github.com/LandRegistry/system-of-record

- A Redis queue.  Redis needs to be installed and a queue setup to store the messages.  See
  the environment.sh file for the name of the queue.

- Python modules listed here: https://github.com/LandRegistry/mint/blob/master/requirements.txt


# Get started

Install the python modules within requirements.txt.  Recommend doing this in a virtual environment.  If pip is
installed, you can type "pip install -r requirements.txt"

Run the server

```
    ./run_dev.sh
```

#Test that it works

```
    python test_post_to_mint.py
```
This fires a quick get to test the service is there, then posts a test title.


# Audit

The audit trail gets logged out to ```audit.log``` currently, and a sample successful edit would be logged like this:

```
Audit start 1403519208
Message: OK
Status code: 200
Diff:
--- a
+++ b
{
 u'title_number': u'THX015',
 u'foo': u'bar55',
}
Audit end 1403519208
```
