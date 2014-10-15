import unittest
import mock
import requests
from themint import app
import json

from themint import server
from datatypes.exceptions import DataDoesNotMatchSchemaException


class MintTestCase(unittest.TestCase):
    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_server(self):
        self.assertEqual((self.app.get('/')).status, '200 OK')

    def test_get_not_allowed(self):
        self.assertEqual((self.app.get('/titles/DN1234')).status, '405 METHOD NOT ALLOWED')

    def post_to_mint(self, data):
        #does not 'mint' anything provided the test environment variables remain blank.
        headers = {'content-type': 'application/json; charset=utf-8'}
        return self.app.post('/titles/dn1234', data=json.dumps(data, encoding='utf-8'), headers=headers)

    def test_error_upon_incorrect_json_schema(self):
        data = {}
        res = self.post_to_mint(data)
        self.assertEqual(res.status, '400 BAD REQUEST')

    def test_for_correct_response_upon_successful_post(self):
        response = requests.get("https://raw.githubusercontent.com/LandRegistry/generate-test-data/master/sample_titles/title-full.json")
        data = response.json()
        self.assertEqual(self.post_to_mint(data).status, '201 CREATED')

    @mock.patch('redis.Redis.info')
    def test_health(self, mock_info):
        self.assertEqual((self.app.get('/health')).status, '200 OK')

