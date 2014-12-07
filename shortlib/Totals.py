#!/usr/bin/env python

from Database import Database as db
from Url import Url


class Totals():

    def __init__(self):
        return

    def get_all(self):
        total4 = 0
        total6 = 0
        totalhits = db.query_db('select sum(hits4) as total4, sum(hits6) as total6 from hits')
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
        items["Users"] = db.query_db('select count(*) as users from users')[0]["users"]
        return items

    def get_all_rows(self):
        rows = []
        totals = self.get_all()
        for key in totals:
            rows.append({"item": key, "total": totals[key]})
        return rows
