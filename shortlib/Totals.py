#!/usr/bin/env python3

from typing import Dict, List

from .Database import Database as db
from .Url import Url


class Totals:
    def get_all(self) -> Dict:
        total4: int = 0
        total6: int = 0
        totalhits: List = db.query_db(
            "select sum(hits4) as total4, sum(hits6) as total6 from hits"
        )
        if len(totalhits) > 0:
            db_total4 = totalhits[0]["total4"]
            db_total6 = totalhits[0]["total6"]
            if db_total4:
                total4 = int(db_total4)
            if total6:
                total6 = int(db_total6)
        items: Dict = {}
        items["Hits"] = total4 + total6
        items["Hit IPv4"] = total4
        items["Hit IPv6"] = total6
        items["URLs"] = Url.total()
        users: List = db.query_db("select count(*) as users from users")
        items["Users"] = users[0]["users"]
        return items

    def get_all_rows(self) -> List:
        rows: List = []
        totals = self.get_all()
        for key in totals:
            rows.append({"item": key, "total": totals[key]})
        return rows
