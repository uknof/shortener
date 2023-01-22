#!/usr/bin/env python

import os
import sys

testdir = os.path.dirname(__file__)
srcdir = ".."
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest

from shortlib import Url


class UrlTest(unittest.TestCase):
    def setUp(self) -> None:
        return

    def tearDown(self) -> None:
        return

    def test_urlvalidYes(self) -> None:
        self.assertTrue(Url.url_valid("http://bbc.co.uk/"))

    def test_urlvalidNo(self) -> None:
        self.assertFalse(Url.url_valid("http//bb_/c.co.uk/"))


if __name__ == "__main__":
    unittest.main()
