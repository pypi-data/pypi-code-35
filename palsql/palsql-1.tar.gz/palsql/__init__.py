import sqlite3

class db:
	def __init__(self, dbname):
		self.conn = sqlite3.connect(dbname)
		self.cur = self.conn.cursor()

	def read(self, command, flat=True):
		self.cur.execute(command)
		f = self.cur.fetchall()
		if not f or not flat:
			return f
		else:
			if len(f[0]) == 1:
				f = [i[0] for i in f]
				if len(f) == 1:
					f = f[0]
			return f

	def read1(self, command):
		self.cur.execute(command)
		f = self.cur.fetchone()
		if len(f) == 1:
			f = f[0]
		return f
	
	def write(self, command):
		self.cur.execute(command)
		self.cur.commit()

	def __del__(self):
		self.conn.close()

