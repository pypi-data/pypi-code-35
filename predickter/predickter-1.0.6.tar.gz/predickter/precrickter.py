import requests
import time
from bs4 import BeautifulSoup

class Precrickter():
	def __init__(self):
		pass

	def crwal(self,url):
		try:
			r = requests.get(url).json()
			return r
		except Exception: 
			raise
	#live matches
	def livematches(self):
		from pycricbuzz import Cricbuzz
		c = Cricbuzz()
		#currect matches
		currect_matches=c.matches()
		"""for match in currect_matches:
			if match['official']==None:
				match['official']='None'"""
		return currect_matches
	#livescore of each match can get by passing id
	def liveScore(self,id):
		from pycricbuzz import Cricbuzz
		c = Cricbuzz()
		#match_id
		livescore=c.livescore(id)
		#print(livescore)
		return livescore
	#score of each match can get by passing id
	def scoreboard(self,id):
		from pycricbuzz import Cricbuzz
		c = Cricbuzz()
		#match_id
		scoreboard=c.scorecard(id)
		#print(scoreboard)
		return scoreboard

	#livecommentary of each match can get by passing id
	def livecommentary(self,id):
		from pycricbuzz import Cricbuzz
		c = Cricbuzz()
		#match_id
		commentary=c.commentary(id)
		return commentary

	#Matchdetails of each match can get by passing id
	def matchdetails(self,id):
		from pycricbuzz import Cricbuzz
		c = Cricbuzz()
		#match_id
		matchdetails=c.matchinfo(id)
		return matchdetails
