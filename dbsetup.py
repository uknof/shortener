#!/usr/bin/env python

from shortlib import Database as db
from shortlib import User
import random
import ipaddr
import string

def main():

    if db.exists() is True:
        p = db.path()

        print ""
        print "Database already exists: %s" % (p)
        print 
        exit(1)

    print ""
    print "Creating database..."
    db.create()
    print ""
    username = "admin"
    password =  ''.join(random.choice(string.lowercase) for i in range(8))
    newuser = User.create(username, password)
    print "New user '%s' created with password '%s'" % (username, password)

    return

if __name__ == '__main__':
    main()