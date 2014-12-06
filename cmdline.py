#!/usr/bin/env python

from shortlib import User, Url
import shortlib.Database as db
import json

print db.query_db("select * from users")
exit(0)

urls = Url.get_all()
print json.dumps([dict(url.__dict__) for url in urls])

#print Url("djcry")


if User.exists("nat"):
    User.delete("nat")

x = User.create("nat","abc123")

authed = User.authenticate("nat","abc123")
print authed.username
