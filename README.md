
# What?

Service to create new versions of a title, hashed and signed.

# Get started

    ./manage.py runserver
    curl -X POST -H 'Content-Type: application/json' http://0.0.0.0:5000/entries \
        -d '{"id":"'$(uuidgen)'","created_date":"'$(date +%Y-%m-%d)'"}'
    curl http://0.0.0.0:5000/entries
    # Record the 'id' of the entry, and use it to update the newly-created entry, e.g. 'be4bcd79-1243-4d39-bfac-e59e3b78b008'
    curl -X POST -H 'Content-Type: application/json' http://0.0.0.0:5000/entries \
        -d '{"id":"be4bcd79-1243-4d39-bfac-e59e3b78b008","created_date":"'$(date +%Y-%m-%d)'"}'
    curl http://0.0.0.0:5000/entries

Yields:

```
[
   {
      "_id":{
         "$oid":"539ef81b2e4733688f58c3d3"
      },
      "created_date":{
         "$date":1402876800000
      },
      "id":"be4bcd79-1243-4d39-bfac-e59e3b78b008",
      "md5sum":"hqskqrp2iru249az"
   },
   {
      "_id":{
         "$oid":"539ef9882e47336a0240cb02"
      },
      "created_date":{
         "$date":1402876800000
      },
      "id":"be4bcd79-1243-4d39-bfac-e59e3b78b008",
      "md5sum":"2xhy01opkf9dtdfm",
      "previous":"hqskqrp2iru249az"
   }
]
```
