import requests
import time

class Precrickter():
	def __init__(self):
		pass

	def crwal(self,url):
		try:
			r = requests.get(url).json()
			return r
		except Exception: 
			raise

	def livemathes(self):
		from pycricbuzz import Cricbuzz
		c = Cricbuzz()
		#currect matches
		currect_matches=c.matches()
		for match in currect_matches:
			if match['official']==None:
				match['official']='None'
		return currect_matches

	

