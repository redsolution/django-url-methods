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

    def tearDown(self):
        pass
