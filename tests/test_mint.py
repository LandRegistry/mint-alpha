import unittest
import mock

from themint import server


class MintTestCase(unittest.TestCase):
    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_server(self):
        self.assertEqual((self.app.get('/')).status, '200 OK')

    def test_get_not_allowed(self):
        self.assertEqual((self.app.get('/titles/DN1234')).status, '405 METHOD NOT ALLOWED')

    @mock.patch('redis.Redis.info')
    def test_health(self, mock_info):
        self.assertEqual((self.app.get('/health')).status, '200 OK')
