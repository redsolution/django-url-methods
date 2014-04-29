import unittest
import doctest

import threadmethod
import urlmethods


class Test(unittest.TestCase):

    def test_threadmethod(self):
        doctest.testmod(threadmethod)
        
    def test_urlmethods(self):
        doctest.testmod(urlmethods)
