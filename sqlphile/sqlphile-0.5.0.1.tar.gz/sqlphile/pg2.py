from . import db3
import psycopg2
from .dbtypes import DB_PGSQL, DB_SQLITE3

class open (db3.open):
	def __init__ (self, dbname, user, password, host = '127.0.0.1', port = 5432, dir = None, auto_reload = False):
		if ":" in host:
			host, port = host.split (":")
			port = int (port)
		self.conn = psycopg2.connect (host=host, dbname=dbname, user=user, password=password, port = port)
		self._init (dir, auto_reload, DB_PGSQL)		
		
	def field_names (self):
		return [x.name for x in self.description]
	
	def set_autocommit (self, flag = True):
		self.conn.autocommit = flag


class open2 (open):
	def __init__ (self, conn, pool, dir = None, auto_reload = False):
		self.conn = conn
		self.pool = pool
		self._init (dir, auto_reload, DB_PGSQL)		
	
	def putback (self):
		self.c.close ()
		self.pool.putconn (self.conn)		
		
	def __exit__ (self, type, value, tb):		
		self.putback ()
