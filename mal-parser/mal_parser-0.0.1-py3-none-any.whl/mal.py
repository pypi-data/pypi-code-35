import requests
from bs4 import BeautifulSoup as BeSo


class MALParser:

	@staticmethod
	def command_handler(command, **kwargs):
		return command(kwargs)


def make_request(url, params=None):
	res = requests.get(url=url, params=params)
	bs = BeSo(res.text, 'lxml')

	return bs, res
