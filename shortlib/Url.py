#!/usr/bin/env python3

import random
from sqlite3 import Connection
from typing import Dict, List, Union

import ipaddr  # type: ignore
import rfc3987  # type: ignore

from .Database import Database as db


class Url:
    def __init__(self, short: str) -> None:
        rows: List = db.query_db(
            "select *,"
            "(select sum(hits4) from hits where hits.short=urls.short) as hits4,"
            "(select sum(hits6) from hits where hits.short=urls.short) as hits6 "
            "from urls where short = ?",
            [short],
        )
        row: Dict = rows[0]
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

    @staticmethod
    def create(
        short: str,
        dest: str,
        createdby: str,
        custom: str = "",
        notes: str = "",
    ) -> "Url":
        d: Connection = db.get_db()
        d.execute(
            "insert into urls (short,dest,createdon,createdby,custom,notes) "
            "values (?,?,date('now'),?,?,?)",
            [short, dest, createdby, custom, notes],
        )
        d.commit()
        newurl = Url(short)
        return newurl

    @staticmethod
    def delete(short: str) -> None:
        d: Connection = db.get_db()
        d.execute("delete from urls where short = ?", [short])
        d.execute("delete from hits where short = ?", [short])
        d.commit()

    def hits(self) -> List:
        h: List = db.query_db(
            "select * from hits where short=? order by hitdate desc",
            [self.short],
        )
        return h

    @staticmethod
    def get_all(createdby: str = "") -> List:
        urls: List = []
        if not createdby:
            urlrows = db.query_db("select short from urls")
        else:
            urlrows = db.query_db(
                "select short from urls where createdby = ?", [createdby]
            )
        for row in urlrows:
            url: Url = Url(row["short"])
            urls.append(url)
        return urls

    def hits_record(self, sourceip: str) -> None:
        d: Connection = db.get_db()
        ip = ipaddr.IPAddress(sourceip)
        hittoday: List = db.query_db(
            "select * from hits where short=? and hitdate=date('now')",
            [self.short],
        )
        hitfield: str = "hits%s" % (ip.version)
        # update hit counters
        if len(hittoday) == 0:
            d.execute(
                "insert into hits (short,hitdate,%s) values (?,date('now'),1)"
                % (hitfield),
                [self.short],
            )
        else:
            d.execute(
                "update hits set %s=%s+1 where short=? and hitdate=date('now')"
                % (hitfield, hitfield),
                [self.short],
            )
        d.commit()

    @staticmethod
    def match(matchurl: str) -> Union["Url", None]:
        short: str = matchurl.lower()
        match: List = db.query_db(
            "select short from urls where (short=? or custom=?)",
            [short, short],
        )
        if len(match) == 0:
            return None
        return Url(match[0]["short"])

    @staticmethod
    def total() -> List:
        urls: List = db.query_db("select count(*) as urls from urls")
        return urls[0]["urls"]

    @staticmethod
    def unique_short() -> str:
        match: bool | List | None = True
        while match:
            short: str = "".join(
                random.choice(
                    [
                        "b",
                        "c",
                        "d",
                        "f",
                        "g",
                        "h",
                        "j",
                        "k",
                        "m",
                        "n",
                        "p",
                        "q",
                        "r",
                        "s",
                        "t",
                        "v",
                        "w",
                        "x",
                        "y",
                        "z",
                    ]
                )
                for i in range(5)
            )
            match = db.query_db("select * from urls where short=?", [short])
        return short

    @staticmethod
    def url_valid(url: str) -> bool:
        if rfc3987.match(url, rule="URI"):
            return True
        return False
