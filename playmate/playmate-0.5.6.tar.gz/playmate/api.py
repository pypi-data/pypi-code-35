from aiohttp import ClientResponseError, ClientSession, ClientTimeout
from bs4 import BeautifulSoup, SoupStrainer
from playmate.scraper import Scraper_
from playmate import lists, settings, utils
from urllib.parse import parse_qs, quote_plus, urlparse

import asyncio
import functools
import logging as log

_pruned = utils.pruned(unwanted_keys=settings.UNWANTED_KEYS)

class PlayMate(Scraper_):
	__sem_http_connections__ = asyncio.BoundedSemaphore(40)

	def __init__(self, headers=utils.default_headers(), timeout=180, hl='en', gl='us'):
		self._headers = headers
		self._timeout = ClientTimeout(total=timeout)
		self._params = dict(hl=hl, gl=gl)
		self._session = ClientSession(
			headers=self._headers,
			timeout=self._timeout
		)

	async def __aenter__(self):
		return self

	async def __aexit__(self, *err):
		await self.close()

	async def close(self):
		if self._session and not self._session.closed:
			try:
				await self._session.close()
			except:
				log.warning('session already closed')
			finally:
				self._session = None
    
	async def send_request(self, method, url, data=None, params={}, allow_redirects=False) -> str:
		options = dict(
			method=method,
			url=url,
			params=params,
			data=utils.generate_post_data() if not data and method == 'POST' else data,
			allow_redirects=allow_redirects
		)
		async with self.__class__.__sem_http_connections__:
			log.info('sending request to url: {} {}'.format(method, url))
			async with self._session.request(**options) as response:
				response.raise_for_status()
				return await response.text()
	
	@_pruned
	async def get_app_details(self, app_id):
		url = utils.build_url('details', app_id)

		awaitable_process = functools.partial(self.send_request, 'GET', url, params=self._params)
		result = await self.__parse_fetched_response__(awaitable_process, multi=False)
		if not result:
			log.warning('no data found for app_id: {}'.format(app_id))
			return {}
		
		_, app_json = result
		app_json.update({
			'app_id': app_id,
			'url': url
		})
		return app_json

	@_pruned
	async def get_apps(self, coln_id, catg_id, max_page=1):
		if not (1 <= max_page <= settings.SEARCH_MAX_PAGE):
			raise ValueError('max_page: {} should be between 1 and {}'.format(
				max_page,
				settings.SEARCH_MAX_PAGE
			))
			
		coln_name = coln_id if coln_id.startswith('promotion') else lists.COLLECTIONS.get(coln_id)
		if coln_name is None:
			raise ValueError('INVALID_COLLECTION_ID: {coln}'.format(
				coln=coln_id
			))

		catg_name = '' if catg_id is None else lists.CATEGORIES.get(catg_id)
		if catg_name is None:
			raise ValueError('INVALID_CATEGORY_ID: {catg}'.format(
				catg=catg_id
			))

		url = utils.build_collection_url(catg_name, coln_name)
		
		tasks = map(lambda page: self.__parse_fetched_response__(functools.partial(
			self.send_request, 
			'POST', 
			url, 
			utils.generate_post_data(settings.NUM_RESULTS, page=page), 
			params=self._params)
		), range(max_page))

		task_results = await asyncio.gather(*tasks)
		if not task_results:
			log.warning('no apps found for coln_id: {} and catg_id: {}'.format(
				coln_id, catg_id
			))
			return []
		
		return self.__prune_duplicates__([
			app for _, apps in task_results for app in apps
		])
	
	@_pruned
	async def get_similar_apps(self, app_id):
		url = utils.build_url('similar', app_id)
		
		awaitable_process = functools.partial(self.send_request, 'GET', url, params=self._params, allow_redirects=True)
		result = await self.__parse_fetched_response__(awaitable_process)
		if not result:
			log.warning('no similar apps found for app_id: {}'.format(app_id))
			return []
		
		_, apps = result
		return self.__prune_duplicates__(apps)
	
	@_pruned
	async def search_apps(self, term, max_page=1):
		if not (1 <= max_page <= settings.SEARCH_MAX_PAGE):
			raise ValueError('max_page: {} should be between 1 and {}'.format(
				max_page,
				settings.SEARCH_MAX_PAGE
			))
		url = '{url}?c=apps&q={query}'.format(
			query=quote_plus(term),
			url=settings.SEARCH_URL
		)
		awaitable_process = functools.partial(self.send_request, 'GET', url, params=self._params)
		result = await self.__parse_fetched_response__(awaitable_process)
		if not result:
			log.warning('no serach results found for term: {}'.format(term))
			return []
		
		soup, apps = result
		search_params = self.__get_paginated_search_params__(soup, max_page)
		if not search_params:
			return apps
		
		tasks = [
			self.__parse_fetched_response__(functools.partial(
				self.send_request,
				'POST',
				search_params.get('url'), 
				data, 
				params=self._params
			))
			for data in search_params.get('datas')
		]
		task_results = await asyncio.gather(*tasks)
		if not task_results:
			return apps

		for _, tapps in task_results:
			apps.extend(tapps)
		
		return self.__prune_duplicates__(apps)

	@classmethod
	def __retrieve_search_params__(cls, soup):
		if not soup:
			return None
		href = soup[0].attrs['href']
		return parse_qs(urlparse(href).query)

	@classmethod
	def __get_paginated_search_post_data__(cls, clp, page):
		return dict(
			start=page * settings.SEARCH_RESULTS,
			num=settings.SEARCH_RESULTS,
			numChildren=0,
			pagTok=settings.PAGE_TOKENS[page],
			clp=clp,
			pagtt=3,
			cctcss='square-cover',
			cllayout='NORMAL',
			ipf=1,
			xhr=1
		)

	@classmethod
	def __get_paginated_search_params__(cls, soup, max_page):
		if max_page == 1:
			return None
		search_configs = cls.__retrieve_search_params__(soup.select('[data-uitype="291"]'))
		if not search_configs:
			log.warning('unable to retrieve gsr value for fetching next pages')
			return None
		post_data_gen = functools.partial(cls.__get_paginated_search_post_data__, search_configs.get('clp'))
		return dict(
			url=settings.SEARCH_PAGINATED_URL.format(gsr=search_configs.get('gsr')),
			datas=[ post_data_gen(page) for page in range(max_page-1) ]
		)

	@classmethod
	async def __parse_fetched_response__(cls, awaitable_process, multi=True):
		soup = None
		try:
			response = await awaitable_process()
			soup = BeautifulSoup(response, 'lxml')
		except ClientResponseError:
			log.exception('no records returned')
		if soup is None:
			return None

		if multi:
			opt = list(map(
				utils.parse_card_info, 
				soup.select('div[data-uitype="500"]')
			))
		else:
			opt = utils.parse_app_details(soup)

		return (soup, opt)

	@classmethod
	def __prune_duplicates__(cls, vals):
		app_ids = set(filter(lambda i: i, map(
			lambda v: v.get('app_id'), vals
		)))

		if len(app_ids) == len(vals):
			return vals

		unique_vals = []
		for app in vals:
			app_id = app.get('app_id')
			if app_id in app_ids:
				unique_vals.append(app)
				app_ids.discard(app_id)
		
		return unique_vals


__all__ = [
	'PlayMate'
]