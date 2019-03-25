import time
from ..utils import Get


__all__ = ["runZhiHuArticle"]


def _getAuthorNames(name):
    """ 获取作者名字 """
    author_headers = {
        "referer": "https://www.zhihu.com/search?type=content&q=python"
    }

    author_params = {
        "type": "content",
        "q": name,
    }

    author_url = "https://www.zhihu.com/search"

    author_soup = Get(author_url, headers=author_headers, params=author_params).soup
    author_name_json = Get.beautifulJson(
        author_soup.find("script", id="js-initialData").text
    )
    author_names = list(author_name_json['initialState']['entities']['users'])
    return author_names


def _getOneAuthorsArticles(author, wb):
    """ 爬取一个作者的所有文章 """
    ws = Get.excelWrite(workbook=wb, sheetname=f"{author}Articles")
    Get.excelWrite(0, 0, label="文章名", worksheet=ws)
    Get.excelWrite(0, 1, label="文章链接", worksheet=ws)
    Get.excelWrite(0, 2, label="文章摘要", worksheet=ws)

    headers = {
        "referer": f"https://www.zhihu.com/people/{author}/posts"
    }

    # 文章计数
    article_nums = 0
    offset = 0
    page_num = 1

    while True:
        articles_params = {
            "include": "data[*].comment_count,suggest_edit,is_normal,thumbnail_extra_info,thumbnail,can_comment,comment_permission,admin_closed_comment,content,voteup_count,created,updated,upvoted_followees,voting,review_info,is_labeled,label_info;data[*].author.badge[?(type=best_answerer)].topics",
            "offset": str(offset),
            "limit": "20",
            "sort_by": "created",
        }

        articles_url = f"https://www.zhihu.com/api/v4/members/{author}/articles"

        articles_res_json = Get(articles_url, headers=headers, params=articles_params).json

        articles = articles_res_json["data"]
        for article in articles:
            article_nums += 1
            article_title = article["title"]
            article_url = article["url"]
            article_excerpt = article["excerpt"]
            print(article_title)
            Get.excelWrite(article_nums, 0, label=article_title, worksheet=ws)
            Get.excelWrite(article_nums, 1, label=article_url, worksheet=ws)
            Get.excelWrite(article_nums, 2, label=article_excerpt, worksheet=ws)

        offset += 20
        headers["referer"] = f"https://www.zhihu.com/people/{author}/posts?page={page_num}"
        page_num += 1

        articles_is_end = articles_res_json["paging"]["is_end"]
        if articles_is_end:
            break

        # # 爬两页就结束
        # if page_num > 2:
        #     break


def runZhiHuArticle():
    """ 获取一个知乎作者的所有文章名称、链接、及摘要，并存到Excel表里 """
    # Excel
    wb = Get.excelWrite(encoding='ascii')

    # 用户输入知乎作者名
    name = input("请输入作者的名字：")
    # 获取作者url_name
    authors = _getAuthorNames(name)
    if not authors:
        authors = _getAuthorNames(name)
    # 获取作者的所有文章
    for author in authors:
        time.sleep(1)
        _getOneAuthorsArticles(author, wb)

    wb.save(f"zhihu{name}.xls")