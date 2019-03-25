import re
import requests


__all__ = ["runDoubanTop250UseRegexExpression"]


def runDoubanTop250UseRegexExpression():
    """ 利用正则表达式提取电影名称/上映时间/上映地点/电影分类/电影评分 """
    url_list = []

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    }

    for i in range(10):
        url = 'https://movie.douban.com/top250?start=' + str(25*i) + '&filter='
        url_list.append(url)

    for url in url_list:
        response = requests.get(url, headers=headers)
        content = response.text.replace(' ', '').replace('\n', '')
        all_tags = re.findall('.*grid_view.*?(<li>.*</li>)',
                              content, flags=re.S)[0]
        movie_tags = re.findall('<li>.*?</li>', all_tags)
        for movie_tag in movie_tags:
            movie_name = re.findall('.*?class="title">(.*?)<', movie_tag)[0]
            other = re.findall('.*?class="bd".*?<br>(.*?)</p>.*', movie_tag)[0]
            release_date = int(re.findall('\d+', other)[0])
            release_place = re.findall(
                '.*?/(.*?)/', other)[0].replace('&nbsp;', '')
            release_category = re.findall(
                '.*/(.*)', other)[0].replace('&nbsp;', '')
            movie_rate = float(re.findall(
                '.*?rating_num.*?>(.*?)<.*?', movie_tag)[0])
            print(
                (movie_name, release_date, release_place, release_category, movie_rate))
