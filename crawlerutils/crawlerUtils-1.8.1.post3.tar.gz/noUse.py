from crawlerUtils import Get

Get.mongoConnect(mongo_url="mongodb://localhost:27017",
                 mongo_db="crawler_db", username="", password="")
url = "http://books.toscrape.com/"


def crawler(url):
    print(url)
    html = Get(url).html
    css_selector = "article.product_pod"
    books = html.find(css_selector)
    for book in books:
        name = book.xpath('//h3/a')[0].text
        price = book.find('p.price_color')[0].text
        Get.mongoInsertLength(
            {
                "书名": name,
                "价格": price
            }, collection="crawler_collection", length=99
        )
    next_url = html.find('li.next a')
    if next_url:
        next_url = Get.urljoin(url, next_url[0].attrs.get("href"))
        crawler(next_url)


crawler(url)
Get.mongoClose()