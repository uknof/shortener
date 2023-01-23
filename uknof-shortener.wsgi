import sys,os,logging

dir = os.path.dirname(__file__)
sys.path.insert(0, dir)
logging.basicConfig(stream=sys.stderr)
from shortner import app as application
