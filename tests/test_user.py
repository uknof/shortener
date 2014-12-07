#!/usr/bin/env python

import os
import sys
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from shortlib import User
from random import randint

USERPREFIX = "testuser"


class UserTest(unittest.TestCase):

    def setUp(self):
        self.username = "%s%s" % (USERPREFIX, randint(100, 999))
        self.password = "testpass%s" % (randint(100, 999))

    def tearDown(self):
        # remove all testuser* users
        users = User.get_all()
        for u in users:
            if u.username.startswith(USERPREFIX):
                u.delete()

    def test_adminUserExists(self):
        exists = User.exists("admin")
        self.assertTrue(exists)

    def test_randomUserDoesntExists(self):
        randomname = "testrandom%s" % (randint(100, 999))
        exists = User.exists(randomname)
        self.assertFalse(exists)

    def test_getallAtLeastOne(self):
        users = User.get_all()
        self.assertGreater(len(users), 0)

    def test_authenticateCorrect(self):
        self.createTestUser()
        self.assertTrue(User.exists(self.username))
        authuser = User.authenticate(self.username, self.password)
        self.assertEqual(self.username, authuser.username)

    def test_authenticateBadPassword(self):
        self.createTestUser()
        authuser = User.authenticate(self.username, "xxx")
        self.assertIsNone(authuser)

    def test_authenticateEmptyPassword(self):
        self.createTestUser()
        authuser = User.authenticate(self.username, "")
        self.assertIsNone(authuser)

    def test_authenticateEmptyUsername(self):
        authuser = User.authenticate("", "xxx")
        self.assertIsNone(authuser)

    def test_createDelete(self):
        testusername = "testcduser%s" % (randint(100, 999))
        newuser = User.create(testusername, "xxx")
        self.assertIsNotNone(newuser)
        self.assertTrue(User.exists(testusername))
        newuser.delete()
        self.assertFalse(User.exists(testusername))

    def createTestUser(self):
        if User.exists(self.username) is False:
            newuser = User.create(self.username, self.password)


if __name__ == '__main__':
    unittest.main()
