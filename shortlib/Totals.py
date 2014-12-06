#!/usr/bin/env python

import sqlite3
from shortlib import Url

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


class Totals():

    def __init__(self):
        return

    def get_all(self):
        total4 = 0
        total6 = 0
        totalhits = query_db('select sum(hits4) as total4, sum(hits6) as total6 from hits')
        if len(totalhits) > 0:
            total4 = totalhits[0]["total4"]
            total6 = totalhits[0]["total6"]
            if total4 is None:
                total4 = 0
            if total6 is None:
                total6 = 0
        items = {}
        items["Hits"] = total4 + total6
        items["Hit IPv4"] = total4
        items["Hit IPv6"] = total6
        items["URLs"] = Url.total()
        items["Users"] = query_db('select count(*) as users from users')[0]["users"]
        return items

    def get_all_rows(self):
        rows = []
        totals = self.get_all()
        for key in totals:
            rows.append({"item": key, "total":totals[key]})
        return rows
