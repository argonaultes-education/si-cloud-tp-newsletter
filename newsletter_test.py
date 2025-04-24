import flask_unittest
import unittest
from newsletter import app as my_app
import re

class TestWelcome(flask_unittest.ClientTestCase):

    app = my_app 

    def test_welcome_identifier(self, client):
        identifiers = ['az', 'az', 'BB', 'rZ']
        for identifier in identifiers:
            rv = client.get(f'/welcome?identifier={identifier}')
            self.assertInResponse(f'{identifier.lower()}'.encode('UTF-8'), rv)

    def test_welcome_bad_identifier(self, client):
        identifiers = ['a', 'azf', '1341', '12']
        for identifier in identifiers:
            rv = client.get(f'/welcome?identifier={identifier}')
            self.assertInResponse(b'Give your identifier', rv)

    def test_welcome_without_identifier(self, client):
        rv = client.get('/welcome')
        self.assertInResponse(b'Give your identifier', rv)

class TestSubscribe(flask_unittest.ClientTestCase):
    
    app = my_app

    def test_valid_email(self, client):
        emails = ['gael@hotmail.com', 'super@caramail.com', 'gael@argonaultes.fr']
        for email in emails:
            rv = client.get(f'/subscribe?email={email}')
            self.assertTrue(re.search(email, rv.data.decode('UTF-8')), email)

    def test_wrong_email(self, client):
        emails = ['gael@gael.com', 'hello@news.fr', 'thisisnotanemail']
        for email in emails:
            rv = client.get(f'/subscribe?email={email}')
            self.assertFalse(re.search(email, rv.data.decode('UTF-8')), email)


if __name__ == '__main__':
    unittest.main()
