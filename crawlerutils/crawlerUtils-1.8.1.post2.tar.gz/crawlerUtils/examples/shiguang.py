from ..utils import Get
import time


__all__ = ["runShiGuang"]


url_list = [
    'http://www.mtime.com/top/tv/top100/',
]
url_list += [f"http://www.mtime.com/top/tv/top100/index-{str(x)}.html" for x in range(2, 11)]


async def crawler():
    content = ["剧名", "导演", "主演", "简介"]
    while url_list:
        url = url_list.pop(0)
        rhtml = await Get(url).arhtml
        contents = rhtml.find("#asyncRatingRegion", first=True).find("li")
        for li in contents:
            content_dict = {}
            title = li.find("h2", first=True).text
            content_dict[content[0]] = title
            contents = li.find("p")
            for i in range(0, min([3, len(contents)])):
                if contents[i].text.strip():
                    if not contents[i].text.strip()[0].isdigit():
                        if contents[i].text[:2] in content:
                            content_dict[contents[i].text[:2]] = contents[i].text
                        else:
                            content_dict[content[3]] = contents[i].text
            Get.csvWrite(fieldnames=["剧名", "导演", "主演", "简介"], filepath="shiguang.csv", dict_params=content_dict)
    return url


def runShiGuang(coroutine_number=5):
    ''' 使用协程爬取时光电影网top100电影信息 '''
    start = time.time()
    Get.csvWrite(fieldnames=["剧名", "导演", "主演", "简介"], filepath="shiguang.csv")
    results = Get.asyncRun(crawler, coroutine_number)
    for result in results:
        print(result)
    end = time.time()
    print(end - start)
