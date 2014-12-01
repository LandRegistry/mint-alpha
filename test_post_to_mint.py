import json
import requests

#This checks that the Mint service is running.
mint_url = 'http://localhost:8001/'
response = requests.get(mint_url)
print('response from Mint is: ' + response.text)


#This tries to post to the mint, with an example from github.

title_no = 'BD161871'
json_url = "https://raw.githubusercontent.com/LandRegistry/migration-emitter/master/samples/%s.json" % title_no
response = requests.get(json_url)
data = response.json()

title_number = data["title_number"]
mint_post_url = '%stitles/%s' % (mint_url, data['title_number'])
headers = {'content-type': 'application/json; charset=utf-8'}
try:
    print('Going to post to Mint now at %s' % mint_url)
    res = requests.post(mint_post_url, data=json.dumps(data, encoding='utf-8'), headers=headers)
    res.raise_for_status()
    print('Title %s created' % title_number)

except requests.exceptions.HTTPError as e:
    print("HTTP Error %s check the server console" % e)

except Exception as e:
    print("Error!  Check the server console. %s" % e)



