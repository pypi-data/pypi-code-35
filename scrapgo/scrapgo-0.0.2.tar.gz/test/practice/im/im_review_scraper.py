import pandas as pd
import os
import re
import json
from io import BytesIO
from collections import namedtuple, OrderedDict

from scrapgo.scraper import LinkRelayScraper, url, urlpattern, urltemplate
from scrapgo.utils.shortcuts import mkdir_p, cp, parse_query, queryjoin, parse_root


def _get_td(tr, index, parse=True):
    tds = tr('td')
    if tds:
        td = tds[index]
        if parse:
            if td and td.text:
                return td.text.strip()
        else:
            return td


class Iam176ReviewScraper(LinkRelayScraper):
    ROOT_URL = 'http://www.iam176.co.kr/board/board.html?code=iam176_board2'
    REQUEST_DELAY = 0, 1,
    CACHE_NAME = 'IMCACHE'
    HEADERS = {
        'Cookie': '____MSLOG__initkey=0.9432849585157661; db=JyEqM54nxlN98ZnjMQ3N6zoMZuvLw7GtAKuJZgdGxNGS%2F3LFcIXvC5hoLbWUDMu0EuVgny5z1i2HvICTHmMAEmqmDHsfsVOonjX7awQtV0cYHOPxidvVY%2Bxn3CGkheRV; shop_language=kor; MakeshopLogUniqueId=667d8c7b905e7a1ebd99ef3e7c47eb09; ____MSLOG__initday=20190324; _Rk_K_eJ1=%22.%22; member_param=type%3Dboard%26code%3Diam176_image1; MSECURESESSION=56bc6de39559f6cf1610a1a1635944dae0954ff70aacf778a44a3f9b6373692c; viewproduct=%2C003000001279%2C003000001299%2C003000001294%2C; _Rk_K_cA2=%7B%22branduid%22%3A%22344473%22%7D; wcs_bt=s_1a81591b2e88:1553425818'
    }
    LINK_RELAY = [
        urltemplate(
            'http://www.iam176.co.kr/board/board.html?code=iam176_board2&page={page}&board_cate=#board_list_target',
            renderer='list_url_renderer',
            parser='list_parser',
            name='list',
            refresh=True
        ),
        urlpattern(
            r'^/board/board.html\?code=iam176_board2&page=(?P<page>\d+)&type=(?P<type>\w+)&board_cate=&num1=(?P<num1>\d+)&num2=(?P<num2>\d+)&number=(?P<number>\d+)&lock=(?P<lock>\w+)$',
            parser='detail_parser',
            name='detail',
            fields=['code', 'type', 'num1', 'num2', 'number']
        ),
        urlpattern(
            r'^http://board.makeshop.co.kr/board/premium183/iam176_board2/(?P<filename>.+)$',
            parser='image_parser',
            name='image',
            referer='detail',
            refresh=True
        )
    ]

    def list_url_renderer(self, template, context=None):
        start = context['start']
        end = context['end']
        for page in range(start, end+1):
            yield template.format(page=page)

    def list_parser(self, response, match, soup, context):
        table = soup.find('table', summary="No, content,Name,Data,Hits")
        if table is None:
            print('list_parser', response.url)
            return

        def parse_no(tr):
            td = _get_td(tr, 0)
            return td

        def parse_title(tr):
            td = _get_td(tr, 3)
            return td.replace('\n', ' ')

        def parse_author(tr):
            td = _get_td(tr, 4, parse=False)
            authors = td('div', class_='video-writer')
            if authors:
                return authors[0].text.replace('\n', ' ').replace('회원게시글검색', '').strip()
            else:
                return 'Unknown'

        def parse_date(tr):
            td = _get_td(tr, 5)
            return td.strip().replace('/', '-')

        for tr in table('tr'):
            no = parse_no(tr)
            if no is None:
                continue
            yield {
                'no': no,
                'title': parse_title(tr),
                'author': parse_author(tr),
                'published': parse_date(tr),
            }

    def detail_parser(self, response, match, soup, context):
        content_area = soup('div', class_='data-bd-cont')[0]
        content = content_area.text.strip()
        no = match('number')
        return {
            'content': content,
            'no': no,
            'href': response.url
        }

    def image_parser(self, response, match, soup, context):
        return {
            'referer': response.referer,
            'src': response.url
        }


def review(context):
    filname = 'results({start}~{end}).csv'.format(**context)
    save_path = os.path.join(context['save_to'], filname)
    iam = Iam176ReviewScraper()
    r = iam.scrap(context=context)
    df_list = pd.DataFrame(r['list'])
    df_detail = pd.DataFrame(r['detail'])
    df_image = pd.DataFrame(r['image'])
    df = pd.merge(df_list, df_detail)
    df = pd.merge(df, df_image, left_on='href', right_on='referer')

    df.to_csv(save_path)
