from .search_engine import SearchEngine, urlparse, parse_qs, quote_plus

from pyquery import PyQuery as pq
import bs4


class Google(SearchEngine):
    def __init__(self):
        super(SearchEngine, self).__init__()
        self.URL = "https://{domain}/search?q={query}&btnG=Search&gbv=1&num={num}&start={start}"

    def ZINbbc_content2items(self, content):
        bs = bs4.BeautifulSoup(content, "html.parser")
        items = list()
        for child in bs.find(id="main").children:
            if " ".join(child.attrs.get("class", tuple())) == "ZINbbc xpd O9g5cc uUPGi" and child.name == "div":
                items.append(child)
        for item in items:
            result = {}
            a = item.a
            if not a or not a.div:
                continue
            title_list = list(a.div.stripped_strings)
            if len(title_list) == 0:
                continue
            result['title'] = title_list[0]
            href = a.attrs.get("href", "")
            if href:
                url = self.filter_link(href)
                if not url:
                    continue
                result['url'] = url
            else:
                continue
            text_node = item.find(class_="BNeawe s3v9rd AP7Wnd")
            if text_node:
                text = " ".join(text_node.stripped_strings)
            else:
                text = ""
            result['text'] = text
            yield result

    def content2items(self, content):
        pq_content = self.pq_html(content)
        items = list(pq_content('div.g').items())
        if len(items) <= 0:
            for result in self.ZINbbc_content2items(content):
                yield result
        for item in items:
            result = {}
            result['title'] = item('h3.r>a').eq(0).text()
            href = item('h3.r>a').eq(0).attr('href')
            if href:
                url = self.filter_link(href)
                if not url:
                    continue
                result['url'] = url
            else:
                continue
            text = item('span.st').text()
            result['text'] = text
            yield result

    def get_name(self):
        return 'google'

    def get_domain(self):
        return "www.google.com"

    def get_url(self, query, **kwargs):
        query = quote_plus(query)
        start = kwargs.get("start", 0)
        domain = kwargs.get("domain", self.get_domain())
        num = kwargs.get("num", 50)
        url=self.URL.format(domain=domain, query=query, num=num, start=start)
        return url

    def filter_link(self, link):
        """
        Returns None if the link doesn't yield a valid result.
        Token from https://github.com/MarioVilas/google
        :return: a valid result
        """
        try:
            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc:
                return link
            # Decode hidden URLs.
            if link.startswith('/url?'):
                link = parse_qs(o.query)['q'][0]
                # Valid results are absolute URLs not pointing to a Google domain
                # like images.google.com or googleusercontent.com
                o = urlparse(link, 'http')
                if o.netloc:
                    return link
        # Otherwise, or on error, return None.
        except Exception as e:
            raise e

LoadSearchEngine=Google
