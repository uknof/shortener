#!/usr/bin/env python

import os
import sys
from typing import Dict

testdir: str = os.path.dirname(__file__)
srcdir: str = ".."
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest

from shortlib import Totals


class TotalsTest(unittest.TestCase):
    def setUp(self) -> None:
        return

    def tearDown(self) -> None:
        return

    def test_getallAtLeastOne(self) -> None:
        totals: Totals = Totals()
        alltotals: Dict = totals.get_all()
        self.assertGreater(len(alltotals), 0)


if __name__ == "__main__":
    unittest.main()
