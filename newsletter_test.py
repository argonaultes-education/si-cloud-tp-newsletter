import flask_unittest
import unittest
from newsletter import app as my_app


class TestWelcome(flask_unittest.ClientTestCase):

    app = my_app 

    def test_welcome_identifier(self, client):
        identifiers = ['a', 'az', '1341', '12']
        for identifier in identifiers:
            rv = client.get(f'/welcome?identifier={identifier}')
            self.assertInResponse(f'{identifier}'.encode('UTF-8'), rv)

    def test_welcome(self, client):
        rv = client.get('/welcome')
        self.assertInResponse(b'Give your identifier', rv)

if __name__ == '__main__':
    unittest.main()
