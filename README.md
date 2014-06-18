
# What?

Service to create new versions of a title, hashed and signed.

Takes a document of the form:

    {
        "address": "1 low street",
        "title_number": "TN1234567",
        "previous_sha256" : "<excluded for v1 of title>"
        /* ... */
    }

...signs it with a private key, and turns it into:

    {
        "title" : {
            "address": "1 low street",
            "title_number": "TN1234567",
            "previous_sha256" : "<excluded for v1 of title>"
             /* ... */
        },
        "sha256": "<the hash of canonicalised .title field above>",
        "public_key": "<key or link to key>"
    }

...before posting it to the [System Of Record](https://github.com/landregistry/system-of-record).

# Get started

Run the server

    ./manage.py runserver

Post a title

    curl -X POST -H 'Content-Type: application/json' http://0.0.0.0:5000/entries \
        -d '{
        "address": "1 low street",
        "title_number": "TN1234567",
        "previous_sha256" : "<excluded for v1 of title>"
        }'

Check that the title has been successfully added:

    curl http://0.0.0.0:5000/entries

Post an update to the title, e.g. new ownership:

    curl -X POST -H 'Content-Type: application/json' http://0.0.0.0:5000/entries \
        -d '{
        "owner": "the name of the new owner"
        "address": "1 low street",
        "title_number": "TN1234567",
        "previous_sha256" : "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        }'

Verify the new entry:

    curl http://0.0.0.0:5000/entries
