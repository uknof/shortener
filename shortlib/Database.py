#!/usr/bin/env python

import sqlite3
import rfc3987
import os


DATABASE = "urls.db"
SCHEMAFILE = "schema.sql"
DATABASEREQ = 0.1

class Database():

    @staticmethod
    def exists():
        return os.path.isfile(DATABASE)

    @staticmethod
    def path():
        return ""

    @staticmethod
    def get_db():
        db = sqlite3.connect(DATABASE)

        def make_dicts(cursor, row):
            return dict((cursor.description[idx][0], value) for idx, value in enumerate(row))
        db.row_factory = make_dicts
        return db

    @staticmethod
    def query_db(query, args=(), one=False):
        cur = Database.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    @staticmethod
    def create():
        d = Database.get_db()
        with open(SCHEMAFILE, 'rt') as f:
            schema = f.read()
        d.cursor().executescript(schema)
        d.commit()
        print "Empty database %s created" % (DATABASE)

            