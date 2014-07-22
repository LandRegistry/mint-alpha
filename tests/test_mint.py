from themint import server
from themint.mint import Response
import unittest
import json
import mock


class MintTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    @mock.patch("themint.mint.Mint.create")
    def test_search(self, mock_create):
        title_number = 'DN100'
        data = json.dumps({'foo':'bar', 'title_number':title_number})

        mock_create.return_value = Response('success', 200)

        self.app.post(
            '/titles/' + title_number,
            data=data,
            content_type='application/json')

        mock_create.assert_called_with(json.loads(data))
