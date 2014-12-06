#!/usr/bin/env python

import sys, os
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from shortobjs import User
from random import randint

class UrlTest(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return


if __name__ == '__main__':
    unittest.main()
