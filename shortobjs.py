#!/usr/bin/env python

import sqlite3

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
    username = "nat"

class Url():

    def __init__(self, short):
        rows = query_db('select *,(select sum(hits4) from hits where hits.short=urls.short) as hits4,(select sum(hits6) from hits where hits.short=urls.short) as hits6 from urls where short = ?', [short])
        row = rows[0]
        self.custom = row["custom"]
        self.dest = row["dest"]
        self.createdby = row["createdby"]
        self.createdon = row["createdon"]
        self.short = row["short"]
        self.hits4 = row["hits4"]
        self.hits6 = row["hits6"]

    def hits(self):
        h = []
        h = query_db("select * from hits where short=? order by hitdate desc", [self.short])
        return []

    @staticmethod
    def total():
        urls = query_db('select count(*) as urls from urls')[0]["urls"]
        return urls

    @staticmethod
    def match(matchurl):
        short = matchurl.lower()
        match = query_db("select short from urls where (short=? or custom=?)", [short, short])
        if len(match) == 0:
            return None
        return Url(match[0]["short"])


    @staticmethod
    def get_all():
        urls = []
        urlrows = query_db('select short from urls')
        for row in urlrows:
            url = Url(row["short"])
            urls.append(url)
        return urls

    @staticmethod
    def unique_short():
        matches = 1
        while matches == 1:
            short = ''.join(random.choice(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']) for i in range(5))
            matches = query_db("select * from urls where short=?", [short])
        return short
