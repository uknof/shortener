#!/usr/bin/env python

import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from shortlib import Url
from random import randint


class UrlTest(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_urlvalidYes(self):
        self.assertTrue(Url.url_valid("http://bbc.co.uk/"))

    def test_urlvalidNo(self):
        self.assertFalse(Url.url_valid("http//bb_/c.co.uk/"))


if __name__ == '__main__':
    unittest.main()
