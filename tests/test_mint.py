from themint import server
from themint.mint import Response
import unittest
import json
import mock
import os

class MintTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True

        self.app = server.app.test_client()
    
    def test_server(self):
        rv = self.app.get('/')
        assert rv.status == '200 OK'

    def test_get_not_allowed(self):
        rv = self.app.get('/titles/DN1234')
        assert rv.status == '405 METHOD NOT ALLOWED'

    @mock.patch("themint.systemofrecord_command.SystemOfRecordCommand.put")
    def test_create(self, mock_create):

        mock_create.return_value = Response('success', 200)

        path = os.path.dirname(os.path.realpath(__file__))
        data = open('%s/data/create_title.json' % path, 'r').read()

        rv = self.app.post('/titles/DN1234', data=data, content_type='application/json')
        assert rv.status  == '200 OK'

    def test_health(self):
        response = self.app.get('/health')
        assert response.status == '200 OK'
