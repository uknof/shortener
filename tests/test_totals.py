#!/usr/bin/env python

import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from shortlib import Totals


class TotalsTest(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_getallAtLeastOne(self):
        totals = Totals()
        alltotals = totals.get_all()
        self.assertGreater(len(alltotals), 0)

if __name__ == '__main__':
    unittest.main()
