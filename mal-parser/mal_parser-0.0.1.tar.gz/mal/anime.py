from mal.resources import URL
from mal.mal import make_request


class Anime:
	@staticmethod
	def topanime(params):
		bs, res = make_request(URL + 'topanime.php', params=params)
		data = dict()
		data['status'] = res.status_code
		data['data'] = []
		animes = bs.find_all(class_='detail')
		scores = bs.find_all(class_='score')
		data['data_length'] = len(animes)
		for i in range(len(animes)):
			info = animes[i].find(class_='information').text.split('\n')
			data['data'].append({
				'Name': animes[i].find(class_='hoverinfo_trigger').text,
				'Length': info[1].strip(' '),
				'Duration': info[2].strip(' '),
				'Favorited': info[3].strip(' '),
				'Score': scores[i + 1].find(class_='text').text
			})
		return data

	@staticmethod
	def season_anime(params=None):
		url = 'anime/season/'
		if params is not None:
			url += params.get('year') + '/' if params.get('year') is not None else ''
			url += params.get('season') if params.get('year') is not None else ''
		bs, res = make_request(URL + url)
		data = dict()
		data['status'] = res.status_code
		data['data'] = []
		animes = bs.find_all(class_='seasonal-anime')
		data['data_length'] = len(animes)
		for i in range(len(animes)):
			data['data'].append({
				'Name': animes[i].find(class_='link-title').text,
				'Source': animes[i].find(class_='source').text,
				'Genres': list(map(lambda x: x.text.strip('\n'), animes[i].find_all(class_='genre'))),
				'Length': animes[i].find(class_='eps').text.strip('\n'),
				'Favorited': animes[i].find(class_='member').text.strip(' \n'),
				'Score': animes[0].find(class_='score').text.strip(' \n')
			})
		return data
