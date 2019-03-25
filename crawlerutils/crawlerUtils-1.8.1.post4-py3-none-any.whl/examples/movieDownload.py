# 改进方向，多线程，协程, 结果Excel, 因为调用了迅雷服务，所以此程序目前仅适用于Windows64位
from urllib.request import quote
import os
import bs4
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
import threading
import logging
import logging.handlers
import datetime
import requests
from requests.adapters import HTTPAdapter
# from win32com.client import Dispatch   # 在Windows运行请取消此行注释


__all__ = ["doubanRunMain"]


SUPER = requests.Session()
# requests.adapters.DEFAULT_RETRIES = 15
SUPER.mount('http://', HTTPAdapter(max_retries=3))
SUPER.mount('https://', HTTPAdapter(max_retries=3))
SUPER.keep_alive = False


TEXT = ""
RECIPIENT = ""
DOWNLOADLINK = ""
EVENT = threading.Event()  # 生成线程事件实例
DEFAULT_REQUEST_HEADERS = {
    'accept-language': 'zh-CN,zh;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36"+\
        " (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
THREADS = []
MAX_THREADS = 10


def setLog(encoding="utf-8"):
    # 日志器
    logger = logging.getLogger('mylogger')
    logger.setLevel(logging.DEBUG)

    # 每天0点自动切割的磁盘文件日志处理器，记录所有日志消息
    rf_handler = logging.handlers.TimedRotatingFileHandler(
        'all.log', when='midnight', interval=1, backupCount=7,
        atTime=datetime.time(0, 0, 0, 0), encoding=encoding)
    rf_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    # 无限大的磁盘文件日志处理器，只记录Error以上级别消息
    f_handler = logging.FileHandler('error.log', encoding=encoding)
    f_handler.setLevel(logging.ERROR)
    # 格式包含文件名和行号
    f_handler.setFormatter(logging.Formatter(
        "%(asctime)s - %(levelname)s -" +
        " %(filename)s[:%(lineno)d] - %(message)s"))

    # 流处理器，输出到stdout，输出所有INFO级别以上消息
    sc_handler = logging.StreamHandler()
    sc_handler.setLevel(logging.INFO)
    sc_handler.setFormatter(logging.Formatter(
        "%(message)s"))

    # 把处理器添加给日志器
    logger.addHandler(rf_handler)
    logger.addHandler(f_handler)
    logger.addHandler(sc_handler)

    return logger


def overtimeTimer(clock=10):
    global EVENT
    count = 0
    EVENT.set()   # 先设置标志位,代表绿灯
    while True:
        if EVENT.is_set():   # 改成红灯
            if count > clock:
                EVENT.clear()    # 清除标志位，变成红灯
                break
        else:
            break

        time.sleep(1)
        count += 1


def intimeDoing(prompt=""):
    global EVENT
    global RECIPIENT

    while True:
        if EVENT.is_set():   # 有标志位，代表是绿灯
            RECIPIENT = input(prompt)
            EVENT.clear()


def intimeDownload(movie="", downloadlink="", i=0, final=""):
    global TEXT
    logger.info(f"\n\n{movie}")
    if i == 0:
        TEXT += f"{movie}" + "<br>"
    else:
        TEXT += f"<br/><br/>{movie}<br/>"
    for f in final:
        downloadlink = getLink(f)
        if downloadlink:
            logger.info(f"\n{f}下载链接：\n" + downloadlink)
            TEXT += f"<br/>{f}下载链接：<br/>"
            TEXT += downloadlink + "<br>"
            logger.debug("\n")


def sendMail(text="", prompt="", subj=""):
    logger.debug(f"开始发送邮件，邮件文本：\n{text}")
    global RECIPIENT

    overtime = threading.Thread(target=overtimeTimer, args=(60,))
    overtime.start()
    intime = threading.Thread(target=intimeDoing, args=(prompt,))
    intime.setDaemon(True)
    intime.start()
    overtime.join()
    recipient = RECIPIENT
    if not recipient:
        recipient = input("请输入收件人邮箱：")
    qqmail = smtplib.SMTP_SSL("smtp.qq.com", 465)
    account = input("请输入你的qq邮箱账号：")
    password = input("请输入与你的qq邮箱授权码：")
    qqmail.login(account, password)
    sender = "Tyrone-Zhao"
    recipients = recipient.split(" ")

    message = MIMEText(text, "html", "utf-8")
    message['From'] = formataddr([sender, account])
    message["Subject"] = Header(subj, "utf-8")
    message["To"] = Header(recipient, "utf-8")

    try:
        qqmail.sendmail(account, recipients, message.as_string())
    except BaseException:
        logger.exception('对不起，发送失败！')
    qqmail.quit()


def addTasktoXunlei(down_urls):
    o = Dispatch("ThunderAgent.Agent64.1")
    course_path = os.getcwd()
    for d in down_urls:
        # AddTask("下载地址", "另存文件名", "保存目录","任务注释","引用地址",
        # "开始模式", "只从原始地址下载","从原始地址下载线程数")
        o.AddTask(d, '', course_path, "", "", -1, 0, 5)
    o.CommitTasks()


def downloadRequests(_):
    ''' 下载链接页面的内容 '''
    logger.info(f"\n\n开始启动迅雷下载链接，当前链接为：\n{_}")
    addTasktoXunlei(_)


def getDownloadLink(movie="", downloadlink=""):
    link_list = []
    logger.info(f"\n\n开始从各大网站获取下载链接，电影名称--{movie}\n")

    try:
        downloadlink1 = getDownloadLinkYangGuang(movie)
        link_list.append(downloadlink1.lstrip("\n"))
        logger.info(f"从阳光电影获取下载链接完毕，当前下载链接：\n{downloadlink1}")
    except BaseException:
        logger.exception("从阳光电影获取下载链接失败！")

    try:
        downloadlink2 = searchMovie993dy(movie)
        link_list.append(downloadlink2.lstrip("\n"))
        logger.info(f"从993dy获取下载链接完毕，当前下载链接：\n{downloadlink2}")
    except BaseException:
        logger.exception("从993dy获取下载链接失败！")

    try:
        downloadlink3 = searchMovieLvYa(movie)
        link_list.append(downloadlink3.lstrip("\n"))
        logger.info(f"从LvYa获取下载链接完毕，当前下载链接：\n{downloadlink3}")
    except BaseException:
        logger.exception("从LvYa获取下载链接失败！")

    try:
        downloadlink4 = searchCiLi(movie)
        link_list.append(downloadlink4.lstrip("\n"))
        logger.info(f"从磁力搜索获取下载链接完毕，当前下载链接：\n{downloadlink4}")
    except BaseException:
        logger.exception("从磁力搜索获取下载链接失败！")

    logger.debug(f"开始下载链接整合，当前状态：\n{link_list}")
    result = []
    for link in link_list:
        link = link.split('\n')
        for l in link:
            if l:
                result.append(l + "\n")

    result = list(set(result))
    downloadlink = "".join(result)

    logger.info(f"完成下载链接整合，当前状态：\n{downloadlink}")
    if len(result) < 2:
        logger.info("""此资源为稀有资源，启动超级搜索功能！""")
        logger.debug(f"下载链接小于两条，开始获取无头网站，当前下载链接：\n{downloadlink}")
        result += searchMovieDygod(movie)
        logger.debug(f"无头Dygod下载链接获取完成，当前下载链接：\n{downloadlink}")

    return downloadlink, result


def searchCiLi(movie, downloadlink=""):
    logger.info(f"从磁力搜索获取下载链接，电影名称--{movie}，当前下载链接：\n{downloadlink}")
    res = SUPER.get(
        "https://www.cilimao.cc/search?word=" + movie + "&page=1",
        timeout=(5, 60))
    res.encoding = "utf-8"
    bsmovie = bs4.BeautifulSoup(res.text, "html.parser")
    link = bsmovie.select("a.Search__result_title___24kb_")
    # 如果不存在搜索结果
    for l in link:
        if "information" in l.get("href"):
            finallink = "https://www.cilimao.cc" + l.get("href")
            res = SUPER.get(finallink, timeout=(5, 60))
            res.encoding = "utf-8"
            bsmovie = bs4.BeautifulSoup(res.text, "html.parser")
            link = bsmovie.select("a.Information__magnet___vubvz")
            downloadlink += link[0].get("href") + "\n"
            break

    return downloadlink.strip("址：\n").strip("址：").strip()


def searchMovie993dy(movie, downloadlink=""):
    logger.info(f"从993dy网站开始下载电影，电影名称--{movie}，当前下载链接：\n{downloadlink}")
    res = SUPER.post(
        "https://www.993dy.com/index.php?m=vod-search",
        data={"wd": movie},
        headers=DEFAULT_REQUEST_HEADERS,
        timeout=(5, 120)
    )
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    try:
        a = soup.find("ul", class_="img-list").find_all("a")
    except AttributeError:
        return downloadlink
    links = []
    if a:
        for b in a:
            res2 = SUPER.get("https://www.993dy.com" + b["href"],
                             headers=DEFAULT_REQUEST_HEADERS,
                             timeout=(5, 60))
            soup2 = bs4.BeautifulSoup(res2.text, "html.parser")
            divs = soup2.find_all("div", class_="mox")
            for di in divs:
                links.extend(di.find_all("script"))
    for l in links:
        co = l.text
        pb = index_of_str(co, "downurls=")
        pe = index_of_str(co, "downarr=")
        co = co[pb:pe]
        p1 = index_of_str(co, "thunder://")
        if p1:
            p2 = index_of_str(co[p1:], '#')
            downloadlink += co[p1:p1+p2] + "\n"
            downloadlink = findAllLinks(co[p1+p2:], p1, p2, downloadlink)
    logger.debug(f"获取到下载链接：\n{downloadlink}")

    return downloadlink


def index_of_str(s1, s2):
    '''
        索引字符串再另一个字符串中第一次出现的位置，可以用str.rfind代替
        s1为长字符串，s2为短字符串，如果s1被切片后传入函数
        那么s2在原s1中的位置应该再加上切片的起始位置，可用str.rfind替换
    '''
    lt = s1.split(s2, 1)
    if s2 not in s1:
        return None
    elif len(lt) == 1:
        return -1
    return len(lt[0])


def findAllLinks(co, p1, p2, downloadlink=""):
    pb = index_of_str(co, "$")
    if pb:
        co = co[pb+1:]
    p3 = index_of_str(co, "thunder://")
    if p3:
        p4 = index_of_str(co[p3:], '#')
        downloadlink += co[p3:p3+p4] + "\n"
        findAllLinks(co[p3+p4:], p3, p4, downloadlink)
    return downloadlink


def searchMovieLvYa(movie, downloadlink=""):
    logger.info(f"从LvYa获取下载链接，电影名称--{movie}，当前下载链接：\n{downloadlink}")
    res = SUPER.get(
        "http://www.lvya.cc/search.php?q=" + movie, timeout=(5, 60)
    )
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    link = soup.select("p a")
    for l in link:
        if l.get("href"):
            res = SUPER.get(
                l.get("href").replace("http://www.lvya.cc/",
                                      "http://www.lvya.cc/download/"),
                timeout=(5, 60)
            )
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            link = soup.select("strong")
            for l in link:
                if "迅雷下载" in l.next:
                    downloadlink += l.parent.text[5:] + "\n"
                    break
            break

    return downloadlink


def searchMovieDygod(movie, downloadlink=""):
    logger.info(f"从Dygod网站获取下载链接，电影名称--{movie}，当前下载链接：\n{downloadlink}")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('log-level=3')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.dygod.net/')
    handle = driver.current_window_handle
    handles = driver.window_handles
    for h in handles:
        if h != handle:
            driver.switch_to.window(h)
            driver.close()
    driver.switch_to.window(handle)
    search_box = driver.find_element_by_name('keyboard')
    search_box.send_keys(movie)
    search_button = driver.find_element_by_name("Submit")
    search_button.click()
    handles = driver.window_handles
    for h in handles:
        if h != handle:
            driver.switch_to.window(h)
            soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
    try:
        link = soup.select("a.ulink")
        for l in link:
            if l.get("href"):
                driver.get(
                    "https://www.dygod.net" + l.get("href")
                )
                soup = bs4.BeautifulSoup(driver.page_source, "html.parser")
                driver.quit()
                link = soup.select("a[thunderhref]")
                for l in link:
                    if "迅雷专用高速下载" in l.get("title"):
                        downloadlink += l.get("thunderhref") + "\n"
                        break
                break
    except BaseException as e:
        logger.exception(e)
    return downloadlink


def findLastlinkYangGuang(finallink, lastlink=""):
    ''' 下载链接页面的内容 '''
    res2 = SUPER.get(finallink, timeout=(5, 60))
    res2.encoding = "gb2312"
    soup2 = bs4.BeautifulSoup(res2.text, "html.parser")

    download = soup2.find("tbody").find_all("a")

    if len(download) == 1:
        lastlink += (download[0]["href"]) + "\n"
    elif len(download) > 1:
        lastlink += (download[1]["href"]) + "\n"
    return lastlink


def searchMovieYangGuang(movie, lastlink=""):
    logger.info(f"到阳光电影首页获取下载链接，电影名称--{movie}，当前下载链接：\n{lastlink}")
    ''' 搜索首页是否存在想看的电影 '''
    res = SUPER.get(
        "https://www.ygdy8.com/", timeout=(5, 60)
    )
    res.encoding = "gb2312"
    bsmovie = bs4.BeautifulSoup(res.text, "html.parser")
    for b in bsmovie.find_all("a"):
        if b.string:
            if "《" + movie + "》" in b.string:
                finallink = "http://www.ygdy8.com" + b["href"]
                findlink = findLastlinkYangGuang(finallink)
                if findlink:
                    lastlink += findlink + "\n"

    return lastlink


def getDownloadLinkYangGuang(movie="", downloadlink=""):
    logger.info(f"从阳光电影获取下载链接，电影名称--{movie}，当前下载链接：\n{downloadlink}")
    url = "http://s.ygdy8.com/plus/so.php?typeid=1&keyword="
    try:
        movie_quote = quote(movie.encode("gbk"))
    except UnicodeEncodeError:
        movie_quote = quote(movie.encode("utf-8"))
    final_url = url + movie_quote
    res = SUPER.get(final_url, timeout=(5, 60))
    res.encoding = "gb2312"
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    content = soup.find("div", class_="co_content8")
    if hasattr(content, "text"):
        if "共0页" in content.text:
            # 那么搜索首页最新影片区域
            downloadlink = searchMovieYangGuang(movie)
            if downloadlink:
                downloadlink += "\n"
        else:
            try:
                link = content.find("a")["href"]
            except AttributeError:
                link = ""
            finallink = "http://s.ygdy8.com" + link
            downloadlink = findLastlinkYangGuang(finallink)
    else:
        # 那么搜索首页最新影片区域
        downloadlink = searchMovieYangGuang(movie)
        if downloadlink:
            downloadlink += "\n"

    return downloadlink


def getMovieNameAndPoint(page, choice="", tail=""):
    if choice == "标题":
        data = "a"
        while data:
            if data != "a":
                getOnePageMovie(tail, choice)
                data = "a"
            while not data.isnumeric() and data:
                data = input("请输入要查看的页码，Enter退出：")
            if data:
                tail = "?start=" + str((int(data)-1)*25) + "&filter="
    elif choice == "新片":
        getOnePageMovie("", choice)
    else:
        for i in range(page):
            tail = "?start=" + str(i*25) + "&filter="
            getOnePageMovie(tail, choice)


def getLink(movie="", downloadlink=""):
    downloadlink, _ = getDownloadLink(movie)
    if not downloadlink:
        downloadlink = searchCiLi(movie)

    return downloadlink


def getOnePageMovie(tail="?start=0&filter=", choice=""):
    global TEXT
    global THREADS
    if choice == "新片":
        url = "https://movie.douban.com/chart"

        res = SUPER.get(url, timeout=(5, 60))
        res.encoding = "utf-8"
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("tr", class_="item")
        result = []
        final_title = []
        number = 0
        for item in items:
            number += 1
            name = item.find("div", class_="pl2").find("a").text.\
                replace("\n", "").strip()
            name = " / ".join([n.strip() for n in name.split(" / ")])
            rating = item.find("span", class_="rating_nums").text
            link = item.find("a")["href"]
            pl = item.find("p", class_="pl").text
            result.append(f"{number}.{name} -- {rating}\n{pl}\n{link}")
            final_title.append(name.replace("(港 / 台)", "").
                               replace("(港/台)", "").replace("(港)", "").
                               replace("(台)", "").split(" / "))

    else:
        url = "https://movie.douban.com/top250" + tail

        res = SUPER.get(url, timeout=(5, 60))
        res.encoding = "utf-8"
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        items = soup.find_all("div", class_="item")
        result = []
        final_title = []
        for item in items:
            number = item.find("em").text
            name = item.find("div", class_="hd").find("a").text.\
                replace("\n", "").replace("\xa0", " ").replace("  ", " ")
            rating = item.find("span", class_="rating_num").text
            try:
                inq = item.find("span", class_="inq").text
            except AttributeError:
                inq = ""
            link = item.find("a")["href"]
            result.append(f"{number}.{name} -- {rating}\n推荐语：{inq}\n{link}")
            final_title.append(name.replace("(港 / 台)", "").
                               replace("(港/台)", "").replace("(港)", "").
                               replace("(台)", "").split(" / "))

    if choice == "标题":
        for r in result:
            logger.info(f"\n{r}")
    if choice == "新片":
        for r in result:
            logger.info(f"\n{r}")
        down = input("""\n是否要发送豆瓣新片的下载链接到邮箱？是请输入1，否则请敲击enter
>>> """)
        if down != "1":
            return
    if choice != "标题":
        for i in range(len(result)):
            intime = threading.Thread(target=intimeDownload,
                                      args=(result[i], i, final_title[i]))
            intime.setDaemon(True)
            THREADS.append(intime)

        while THREADS:
            for i in range(min(len(THREADS), MAX_THREADS)):
                THREADS[i].start()
            for i in range(min(len(THREADS), MAX_THREADS)):
                THREADS[i].join()
            THREADS = THREADS[min(len(THREADS), MAX_THREADS):]


def downloadMovie(movie):
    if not movie:
        movie = pyperclip.paste()
    else:
        downloadlink = ""
        if not downloadlink:
            downloadlink, _ = getDownloadLink(movie)
        if _:
            downloadRequests(_)
        else:
            logger.info("下载链接未找到，抱歉啦！")
            time.sleep(2)


def main():
    movie = input("""想发送豆瓣top250的下载链接到你的QQ邮箱（需要开启smtp并获取授权码），请输入“豆瓣top250”。
想查看豆瓣top250的标题，请输入“豆瓣top250标题”。
想查看豆瓣新片，请输入“豆瓣新片”。
想下载电影，请输入电影名称，如已复制电影名请敲击enter即可。(电影搜索完成后会自动打开迅雷，如果没有弹出下载框，请点击新建任务手动粘贴)
>>> """)
    if movie == "豆瓣top250":
        getMovieNameAndPoint(10)
        sendMail(TEXT, "\n\n豆瓣top250的电影下载链接将被发送至您的邮箱，请在60秒内输入QQ邮箱账号\n" +
                 "多个账号请以空格隔开, 直接敲击enter发送至默认邮箱200612453@qq.com：",
                 "豆瓣电影Top250下载链接")
        movie = ""
    if movie == "豆瓣新片":
        getMovieNameAndPoint(10, "新片")
        if TEXT:
            sendMail(TEXT, "\n\n最新豆瓣影片的电影下载链接将被发送至您的邮箱，请在60秒内输入QQ邮箱账号\n" +
                     "多个账号请以空格隔开, 直接敲击enter发送至默认邮箱200612453@qq.com：",
                     "豆瓣最新影片下载链接")
        movie = ""
    while movie == "豆瓣top250标题":
        getMovieNameAndPoint(10, "标题")
        movie = input("""想下载电影，请输入电影名称，enter退出。
>>> """)
    if movie:
        logger.info(f"\n\n输入的电影名称为：{movie}")
        downloadMovie(movie)


def doubanRunMain():
    logger = setLog()
    try:
        main()
    except BaseException:
        logger.exception("程序异常！")