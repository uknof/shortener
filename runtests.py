#!/usr/bin/env python3

import typing
from shortlib import Database, User
from unittest import TestLoader, TestSuite, TextTestRunner
from tests import test_totals, test_url, test_user

if not Database.exists():
    Database.setup()
    User.setup()

testLoader: TestLoader = TestLoader()
testSuite: TestSuite = TestSuite()

testSuite.addTests(testLoader.loadTestsFromModule(test_totals))
testSuite.addTests(testLoader.loadTestsFromModule(test_url))
testSuite.addTests(testLoader.loadTestsFromModule(test_user))

textRunner: TextTestRunner = TextTestRunner(verbosity=3)
textRunner.run(testSuite)
