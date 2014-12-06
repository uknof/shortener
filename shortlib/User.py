#!/usr/bin/env python

import random
from passlib.hash import pbkdf2_sha256
from Database import Database as db
from Url import Url

class User():

    def __init__(self, username):
        username = username.lower().strip()
        userdb = db.query_db("select * from users where username = ?", [username])
        if len(userdb) == 0:
	       raise Exception("No user '%s' found" % (username))
        self.username = userdb[0]["username"]
        self.logins = userdb[0]["logins"]
        self.last_login = userdb[0]["last_login"]
        self.urlcount = len(Url.get_all(self.username))

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def delete(self):
        d = db.get_db()
        d.execute('delete from users where username = ?', [self.username])
        d.commit()
        return None

    @staticmethod
    def get(username):
        return User(username)

    @staticmethod
    def get_all():
        users = []
        for userrow in db.query_db("select username from users"):
            username = userrow["username"]
            user = User(username)
            users.append(user)
        return users

    @staticmethod
    def exists(username):
        username = username.lower().strip()
        userdb = db.query_db("select * from users where username = ?", [username])
        if len(userdb) == 0:
	    return False
        else:
            return True

    @staticmethod
    def authenticate(username, password):
        username = username.lower().strip()
        if len(username) == 0 or len(password) == 0:
            return None
        userdb = db.query_db("select * from users where username = ?", [username])
        if len(userdb) == 1:       
            # user exists, check the hash
            hash = userdb[0]["password"]
            if pbkdf2_sha256.verify(password, hash):
                d = db.get_db()
                d.execute("update users set logins = logins + 1, last_login = date('now') where username = ?", [username])
                d.commit() 
                return User(username)
        return None

    @staticmethod
    def create(username, password):
        username = username.lower().strip()
        if User.exists(username) is True:
            raise Exception("user '%s' already exists" % (username))
        hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        d = db.get_db()
        d.execute('insert into users (username,password) values (?,?)', [username, hash])
        d.commit()        
        if User.exists(username) is False:
	       raise Exception("created user '%s' does not exist" % (username))
        u = User(username)
        if u is None:
           raise Exception("created user '%s' is None" % (username))
        return u
