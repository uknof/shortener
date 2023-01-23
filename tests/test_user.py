#!/usr/bin/env python

import os
import sys

testdir = os.path.dirname(__file__)
srcdir = ".."
sys.path.insert(0, os.path.abspath(os.path.join(testdir, srcdir)))

import unittest
from random import randint
from typing import List

from shortlib import User

USERPREFIX: str = "testuser"


class UserTest(unittest.TestCase):
    def setUp(self) -> None:
        self.username = "%s%s" % (USERPREFIX, randint(100, 999))
        self.password = "testpass%s" % (randint(100, 999))

    def tearDown(self) -> None:
        # remove all testuser* users
        users: List = User.get_all()
        u: User
        for u in users:
            if u.username.startswith(USERPREFIX):
                u.delete()

    def test_adminUserExists(self) -> None:
        exists: bool = User.exists("admin")
        self.assertTrue(exists)

    def test_randomUserDoesntExists(self) -> None:
        randomname: str = "testrandom%s" % (randint(100, 999))
        exists: bool = User.exists(randomname)
        self.assertFalse(exists)

    def test_getallAtLeastOne(self) -> None:
        users: List = User.get_all()
        self.assertGreater(len(users), 0)

    def test_authenticateCorrect(self) -> None:
        self.createTestUser()
        self.assertTrue(User.exists(self.username))
        authuser: User | None = User.authenticate(self.username, self.password)
        self.assertIsNotNone(authuser)
        assert authuser
        self.assertEqual(self.username, authuser.username)

    def test_authenticateBadPassword(self) -> None:
        self.createTestUser()
        self.assertIsNone(User.authenticate(self.username, "xxx"))

    def test_authenticateEmptyPassword(self) -> None:
        self.createTestUser()
        self.assertIsNone(User.authenticate(self.username, ""))

    def test_authenticateEmptyUsername(self) -> None:
        self.assertIsNone(User.authenticate("", self.password))

    def test_createDelete(self) -> None:
        testusername: str = "testcduser%s" % (randint(100, 999))
        newuser: User | None = User.create(testusername, "xxx")
        self.assertIsNotNone(newuser)
        assert newuser
        self.assertTrue(User.exists(testusername))
        newuser.delete()
        self.assertFalse(User.exists(testusername))

    def createTestUser(self) -> None:
        if User.exists(self.username) is False:
            User.create(self.username, self.password)


if __name__ == "__main__":
    unittest.main()
