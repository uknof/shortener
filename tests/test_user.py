#!/usr/bin/env python

import sys, os
testdir = os.path.dirname(__file__)
srcdir = '..'
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from shortobjs import User
from random import randint

class UserTest(unittest.TestCase):

    def setUp(self):
        self.username = "testuser%s" % (randint(100,999))
        self.password = "testpass%s" % (randint(100,999))

    def test_adminUserExists(self):
        exists = User.exists("admin")
        self.assertTrue(exists)

    def test_randomUserDoesntExists(self):
        randomname = "testrandom%s" % (randint(100,999))
        exists = User.exists(randomname)
        self.assertFalse(exists)

    def test_getallAtLeastOne(self):
        users = User.get_all()
        self.assertGreater(len(users),0)

    def test_createUser(self):
        newuser = User.create(self.username, self.password)
        self.assertIsNotNone(newuser)
        self.assertEqual(self.username, newuser.username)

    def test_authenticateCorrect(self):
        authuser = User.authenticate(self.username, self.password)
        self.assertIsNotNone(authuser)

    def test_authenticateBadPassword(self):
        authuser = User.authenticate(self.username, "xxx")
        self.assertIsNone(authuser)

    def test_createDelete(self):
        testusername = "testcduser%s" % (randint(100,999))
        newuser = User.create(testusername,"xxx")
        self.assertIsNotNone(newuser)
        self.assertTrue(User.exists(testusername))
        User.delete(testusername)
        self.assertFalse(User.exists(testusername))

if __name__ == '__main__':
    unittest.main()
