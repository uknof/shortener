#!/usr/bin/env python

import shortobjs
import json

urls = shortobjs.Url.get_all()
print json.dumps([dict(url.__dict__) for url in urls])

#print shortobjs.Url("djcry")
