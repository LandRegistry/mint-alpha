import unittest
import mock
import os

from themint import server
from themint.mint import Response


class MintTestCase(unittest.TestCase):
    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_server(self):
        self.assertEqual((self.app.get('/')).status, '200 OK')

    def test_get_not_allowed(self):
        self.assertEqual((self.app.get('/titles/DN1234')).status, '405 METHOD NOT ALLOWED')

    @mock.patch("themint.systemofrecord_command.SystemOfRecordCommand.put")
    def test_create(self, mock_create):
        mock_create.return_value = Response('success', 200)

        path = os.path.dirname(os.path.realpath(__file__))
        data = open('%s/data/create_title.json' % path, 'r').read()

        self.assertEqual((self.app.post('/titles/DN1234', data=data, content_type='application/json')).status, '200 OK')

    @mock.patch('redis.Redis.info')
    def test_health(self, mock_info):
        self.assertEqual((self.app.get('/health')).status, '200 OK')
