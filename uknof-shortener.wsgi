import sys,os,logging

os.environ['DATABASE_LOCAL'] = "/var/uknofdb/urls.db"
dir = os.path.dirname(__file__)
sys.path.insert(0, dir)
logging.basicConfig(stream=sys.stderr)
from shortner import app as application
