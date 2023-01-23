#!/usr/bin/env python3

import os
import sqlite3
from sqlite3 import Connection, Cursor
from typing import Any, Dict, List

DATABASEREQ = 0.1


class Database:
    @staticmethod
    def create() -> None:
        d = Database.get_db()
        schema_path: str = os.path.join(
            os.environ["BUILD_DIR"], os.environ["SCHEMAFILE"]
        )
        with open(schema_path, "rt") as f:
            schema: str = f.read()
        d.cursor().executescript(schema)
        d.commit()
        print("Empty database %s created" % (Database.path()))

    @staticmethod
    def exists() -> bool:
        return os.path.isfile(Database.path())

    @staticmethod
    def get_db() -> Connection:
        db: Connection = sqlite3.connect(Database.path())

        def make_dicts(cursor: Cursor, row: str) -> Dict:
            return dict(
                (cursor.description[idx][0], value)
                for idx, value in enumerate(row)
            )

        db.row_factory = make_dicts
        return db

    @staticmethod
    def path() -> str:
        return os.path.join(os.environ["BUILD_DIR"], os.environ["DATABASE"])

    @staticmethod
    def query_db(query: str, args: Any = (), one: bool = False) -> List:
        cur: Cursor = Database.get_db().execute(query, args)
        rv: List = cur.fetchall()
        cur.close()
        return (rv[0] if rv else []) if one else rv

    @staticmethod
    def setup() -> None:
        if Database.exists():
            print("\nUsing existing database: %s\n" % (Database.path()))
            return

        print("\nCreating new database %s..." % (Database.path()))
        Database.create()
