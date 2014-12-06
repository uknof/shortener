#!/usr/bin/env python

import sqlite3
import random
from passlib.hash import pbkdf2_sha256

DATABASE = "urls.db"


def get_db():
    db = sqlite3.connect(DATABASE)

    def make_dicts(cursor, row):
        return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
    db.row_factory = make_dicts
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


class User():

    def __init__(self, username):
        username = username.lower().strip()
        userdb = query_db("select * from users where username = ?", [username])
        if len(userdb) == 0:
	       raise Exception("No user '%s' found" % (username))
        self.username = userdb[0]["username"]
        self.random = ''.join(random.choice(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']) for i in range(5))

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def delete(self):
        db = get_db()
        db.execute('delete from users where username = ?', [self.username])
        db.commit()
        return None

    @staticmethod
    def get(username):
        return User(username)

    @staticmethod
    def get_all():
        users = []
        for userrow in query_db("select username from users"):
            username = userrow["username"]
            user = User(username)
            users.append(user)
        return users

    @staticmethod
    def exists(username):
        username = username.lower().strip()
        userdb = query_db("select * from users where username = ?", [username])
        if len(userdb) == 0:
	    return False
        else:
            return True

    @staticmethod
    def authenticate(username, password):
        username = username.lower().strip()
        if len(username) == 0 or len(password) == 0:
            return None
        userdb = query_db("select * from users where username = ?", [username])
        if len(userdb) == 1:       
            # user exists, check the hash
            hash = userdb[0]["password"]
            if pbkdf2_sha256.verify(password, hash):
                return User(username)
        return None

    @staticmethod
    def create(username, password):
        username = username.lower().strip()
        if User.exists(username) is True:
            raise Exception("user '%s' already exists" % (username))
        hash = pbkdf2_sha256.encrypt(password, rounds=200000, salt_size=16)
        db = get_db()
        db.execute('insert into users (username,password) values (?,?)', [username, hash])
        db.commit()        
        if User.exists(username) is False:
	       raise Exception("created user '%s' does not exist" % (username))
        u = User(username)
        if u is None:
           raise Exception("created user '%s' is None" % (username))
        return u
