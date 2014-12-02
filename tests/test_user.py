import unittest
from ..shortobjs import User
from random import randint

class UserTest(unittest.TestCase):

    def setUp(self):
        self.username = "testuser%s" % (randint(100,999))
        self.password = "testpass%s" % (randint(100,999))

    def blah(self):
        self.assertTrue(False)

    def createUser(self):
        newuser = User.create(self.username, self.password)
        self.assertIsNotNone(newuser)
        self.assertEqual(self.username, newuser.username)

    def authenticateCorrect(self):
        authuser = User.authenticate(self.username, self.password)
        self.assertIsNotNone(authuser)

    def authenticateBadPassword(self):
        authuser = User.authenticate(self.username, "xxx")
        self.assertIsNone(authuser)


if __name__ == '__main__':
    unittest.main()
