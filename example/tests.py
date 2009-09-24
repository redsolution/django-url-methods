import unittest
from django.test import Client

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_views(self):
        client = Client()
        self.assertEqual(client.get('/response').status_code, 200)
        self.assertEqual(client.get('/notfound').status_code, 404)
        self.assertEqual(client.get('/error').status_code, 500)
        self.assertEqual(client.get('/redirect_response').status_code, 302)
        self.assertEqual(client.get('/redirect_notfound').status_code, 302)
        self.assertEqual(client.get('/redirect_redirect_response').status_code, 302)
        self.assertEqual(client.get('/redirect_cicle').status_code, 302)
        self.assertEqual(client.get('/permanent_redirect_response').status_code, 301)
        self.assertEqual(client.get('/http404').status_code, 404)
        self.assertRaises(Exception, client.get, '/http500')
        self.assertEqual(client.get('/request_true_response').content , 'True')
        self.assertEqual(client.get('/request_false_response').content , 'False')
        self.assertEqual(client.get('/doesnotexists').status_code, 404)
        
    def tearDown(self):
        pass
