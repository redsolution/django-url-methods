import unittest
import doctest
from django.test import Client

import threadmethod
import urlmethods

class Test(unittest.TestCase):
    def setUp(self):
        pass

    def test_threadmethod(self):
        doctest.testmod(threadmethod)
        
    def test_urlmethods(self):
        doctest.testmod(urlmethods)

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
        
    def test_local_check(self):
        self.assertEqual(urlmethods.local_check('/response'), True)
        self.assertEqual(urlmethods.local_check('/notfound'), False)
        self.assertEqual(urlmethods.local_check('/error'), False)
        self.assertEqual(urlmethods.local_check('/redirect_response'), True)
        self.assertEqual(urlmethods.local_check('/redirect_notfound'), False)
        self.assertEqual(urlmethods.local_check('/redirect_redirect_response'), True)
        self.assertEqual(urlmethods.local_check('/redirect_cicle'), False)
        self.assertEqual(urlmethods.local_check('/permanent_redirect_response'), True)
        self.assertEqual(urlmethods.local_check('/http404'), False)
        self.assertEqual(urlmethods.local_check('/http500'), False)
        self.assertEqual(urlmethods.local_check('/request_true_response'), True)
        self.assertEqual(urlmethods.local_check('/request_false_response'), True)
        self.assertEqual(urlmethods.local_check('/doesnotexists'), False)

    def tearDown(self):
        pass
