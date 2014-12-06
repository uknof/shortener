#!/usr/bin/env python

import sqlite3
import rfc3987
import random
import ipaddr
from Database import Database as db

class Url():

    def __init__(self, short):
        rows = db.query_db('select *,(select sum(hits4) from hits where hits.short=urls.short) as hits4,(select sum(hits6) from hits where hits.short=urls.short) as hits6 from urls where short = ?', [short])
        row = rows[0]
        self.custom = row["custom"]
        self.dest = row["dest"]
        self.notes = row["notes"]
        self.createdby = row["createdby"]
        self.createdon = row["createdon"]
        self.short = row["short"]
        self.hits4 = row["hits4"]
        if self.hits4 is None:
            self.hits4 = 0
        self.hits6 = row["hits6"]
        if self.hits6 is None:
            self.hits6 = 0

    def hits(self):
        h = []
        h = db.query_db("select * from hits where short=? order by hitdate desc", [self.short])
        return []

    def delete(self):
        db = get_db()
        db.execute("delete from urls where short = ?", [self.short])
        db.execute("delete from hits where short = ?", [self.short])
        db.commit()
        return

    def hits_record(self, sourceip):
        db = get_db()
        ip = ipaddr.IPAddress(sourceip)
        hittoday = db.query_db("select * from hits where short=? and hitdate=date('now')", [self.short])
        hitfield = "hits%s" % (ip.version)
        # update hit counters
        if len(hittoday) == 0:
            db.execute("insert into hits (short,hitdate,%s) values (?,date('now'),1)" % (hitfield), [self.short])
        else:
            db.execute("update hits set %s=%s+1 where short=? and hitdate=date('now')" % (hitfield,hitfield), [self.short])
        db.commit()

        return

    @staticmethod
    def total():
        urls = db.query_db('select count(*) as urls from urls')[0]["urls"]
        return urls

    @staticmethod
    def match(matchurl):
        short = matchurl.lower()
        match = db.query_db("select short from urls where (short=? or custom=?)", [short, short])
        if len(match) == 0:
            return None
        return Url(match[0]["short"])

    @staticmethod
    def get_all(createdby=None):
        urls = []
        if createdby is None:
            urlrows = db.query_db('select short from urls')
        else:
            urlrows = db.query_db('select short from urls where createdby = ?', [createdby])
        for row in urlrows:
            url = Url(row["short"])
            urls.append(url)
        return urls

    @staticmethod
    def unique_short():
        matches = 1
        while matches == 1:
            short = ''.join(random.choice(['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']) for i in range(5))
            matches = db.query_db("select * from urls where short=?", [short])
        return short

    @staticmethod
    def url_valid(url):
        if rfc3987.match(url, rule='URI'):
            return True
        return False

    @staticmethod
    def create(short, dest, createdby, custom='', notes=''):
        d = db.get_db()
        d.execute("insert into urls (short,dest,createdon,createdby,custom,notes) values (?,?,date('now'),?,?,?)", [short, dest,createdby,custom,notes])
        d.commit()
        newurl = Url(short)
        return newurl



