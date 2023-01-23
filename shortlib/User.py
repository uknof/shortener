#!/usr/bin/env python3

import random
import string
from sqlite3 import Connection
from typing import List, Union

from passlib.hash import pbkdf2_sha256

from .Database import Database as db
from .Url import Url


class User:
    def __init__(self, username: str) -> None:
        username = username.lower().strip()
        userdb: List = db.query_db(
            "select * from users where username = ?", [username]
        )
        if len(userdb) == 0:
            raise Exception("No user '%s' found" % (username))
        self.username: str = userdb[0]["username"]
        self.logins: str = userdb[0]["logins"]
        self.last_login: str = userdb[0]["last_login"]
        self.urlcount: int = len(Url.get_all(self.username))

    @staticmethod
    def authenticate(username: str, password: str) -> Union["User", None]:
        username = username.lower().strip()
        if len(username) == 0 or len(password) == 0:
            return None
        userdb: List = db.query_db(
            "select * from users where username = ?", [username]
        )
        if len(userdb) == 1:
            # user exists, check the hash
            phash: str = userdb[0]["password"]
            if pbkdf2_sha256.verify(password, phash):
                d: Connection = db.get_db()
                d.execute(
                    "update users set logins = logins + 1, last_login = date('now') where username = ?",
                    [username],
                )
                d.commit()
                return User(username)
        return None

    @staticmethod
    def create(username: str, password: str) -> "User":
        username = username.lower().strip()
        if User.exists(username) is True:
            raise Exception("user '%s' already exists" % (username))
        phash: str = pbkdf2_sha256.encrypt(
            password, rounds=200000, salt_size=16
        )
        d: Connection = db.get_db()
        d.execute(
            "insert into users (username,password) values (?,?)",
            [username, phash],
        )
        d.commit()
        if User.exists(username) is False:
            raise Exception("created user '%s' does not exist" % (username))
        u: User | None = User(username)
        if not u:
            raise Exception("created user '%s' is None" % (username))
        return u

    def delete(self) -> None:
        d: Connection = db.get_db()
        d.execute("delete from users where username = ?", [self.username])
        d.commit()

    @staticmethod
    def exists(username: str) -> bool:
        username = username.lower().strip()
        userdb: List = db.query_db(
            "select * from users where username = ?", [username]
        )
        if len(userdb) == 0:
            return False
        else:
            return True

    @staticmethod
    def get(username: str) -> "User":
        return User(username)

    def get_id(self) -> str:
        return self.username

    @staticmethod
    def get_all() -> List["User"]:
        users: List = []
        for userrow in db.query_db("select username from users"):
            username: str = userrow["username"]
            user: User = User(username)
            users.append(user)
        return users

    @staticmethod
    def gen_password() -> str:
        return "".join(
            random.choice(string.ascii_letters + string.digits)
            for i in range(25)
        )

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False

    def is_authenticated(self) -> bool:
        return True

    @staticmethod
    def setup() -> None:
        username: str = "admin"
        password: str = User.gen_password()
        if not User.create(username, password):
            raise Exception(f"Failed to create admin user!")
        print("New user '%s' created with password '%s'" % (username, password))
