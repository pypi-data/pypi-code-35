# 爬取QQ音乐周杰伦的歌曲信息
import time
from ..utils import Get


__all__ = ["runQQSinger"]


def getQQMusicGoodComments(url=None, pages=2):
    ''' selenium获取QQ音乐两页精彩评论 '''
    if url:
        driver = Get(url).hdriver
    else:
        driver = Get("https://y.qq.com/n/yqq/song/000xdZuV2LcQ19.html").hdriver
    time.sleep(2)

    for i in range(pages):
        more_button = Get.locateElement(driver, "cs")(".js_get_more_hot")
        more_button.click()
        comments_list = Get.locateElement(driver, "cs")(".js_hot_list")
        # pageSource = driver.page_source # 获取Elements中渲染完成的网页源代码
        # soup = BeautifulSoup(pageSource,'html.parser')  # 使用bs解析网页
        # comments = soup.find('ul',class_='js_hot_list').find_all('li',class_='js_cmt_li') # 使用bs提取元素
        comments = Get.locateElement(comments_list, "cs")(".js_hot_text")

        for co in comments:
            print(f"-------评论-----------------: \n{co.text}")


def getSingerInfoAtQQ(singer_name="周杰伦", song_pages=5, comment_pages=5):
    ''' 爬取QQ音乐上一个歌手的歌曲信息及最新评论信息 '''
    # 把歌曲信息存入Excel
    workbook = Get.excelWrite(encoding='ascii')
    worksheet = Get.excelWrite(workbook=workbook, sheetname='SongSheet')
    Get.excelWrite(0, 0, label="歌曲名", worksheet=worksheet)
    Get.excelWrite(0, 1, label="所属专辑", worksheet=worksheet)
    Get.excelWrite(0, 2, label="播放时长", worksheet=worksheet)
    Get.excelWrite(0, 3, label="播放链接", worksheet=worksheet)
    Get.excelWrite(0, 4, label="歌词", worksheet=worksheet)
    Get.excelWrite(0, 5, label="评论", worksheet=worksheet)

    # 爬取歌曲信息
    num = 0
    singer_link = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    for j in range(song_pages):
        singer_params = {
            "ct": "24",
            "qqmusic_ver": "1298",
            "new_json": "1",
            "remoteplace": "sizer.yqq.song_next",
            "searchid": "63564811682994419",
            "t": "0",
            "aggr": "1",
            "cr": "1",
            "catZhida": "1",
            "lossless": "0",
            "flag_qc": "0",
            "p": str(j+1),
            "n": "20",
            "w": singer_name,
            "g_tk": "776474075",
            "loginUin": "200612453",
            "hostUin": "0",
            "format": "json",
            "inCharset": "utf8",
            "outCharset": "utf-8",
            "notice": "0",
            "platform": "yqq.json",
            "needNewCode": "0"
        }
        json_music = Get(singer_link, params=singer_params).json
        for music in json_music["data"]["song"]["list"]:
            comment_num = 5
            num += 1
            da_da_da = music["name"]
            album = music["album"]["name"]
            duration = str(music["interval"] // 60) + \
                ":" + str(music["interval"] % 60)
            link = "https://y.qq.com/n/yqq/song/" + music["mid"]
            music_id = music["id"]

            # 爬取歌词信息
            params = {
                "nobase64": "1",
                "musicid": music_id,
                "-": "jsonp1",
                "g_tk": "5381",
                "loginUin": "0",
                "hostUin": "0",
                "format": "json",
                "inCharset": "utf8",
                "outCharset": "utf-8",
                "notice": "0",
                "platform": "yqq.json",
                "needNewCode": "0"
            }
            Get.headersAdd({
                "Referer": link
            })
            lyrics_link = f"https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_yqq.fcg"
            lyrics_json = Get(lyrics_link, params=params).json
            lyric = Get.htmlUnescape(lyrics_json["lyric"])

            Get.excelWrite(num, 0, label=da_da_da, worksheet=worksheet)
            Get.excelWrite(num, 1, label=album, worksheet=worksheet)
            Get.excelWrite(num, 2, label=duration, worksheet=worksheet)
            Get.excelWrite(num, 3, label=link, worksheet=worksheet)
            Get.excelWrite(num, 4, label=lyric, worksheet=worksheet)

            # 爬取评论信息
            comment_link = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg"
            comment_id = ""
            reqtype = "1"

            for i in range(comment_pages):
                comment_params = {
                    "g_tk": "776474075",
                    "loginUin": "200612453",
                    "hostUin": "0",
                    "format": "json",
                    "inCharset": "utf8",
                    "outCharset": "GB2312",
                    "notice": "0",
                    "platform": "yqq.json",
                    "needNewCode": "0",
                    "cid": "205360772",
                    "reqtype": reqtype,
                    "biztype": "1",
                    "topid": music_id,
                    "cmd": "8",
                    "needmusiccrit": "0",
                    "pagenum": str(i),
                    "pagesize": "25",
                    "lasthotcommentid": comment_id,
                    "domain": "qq.com",
                    "ct": "24",
                    "cv": "101010",
                }
                comments = Get(comment_link, params=comment_params).json
                if comments['comment'].get("commentlist"):
                    comment_list = comments['comment']['commentlist']
                    lasthot = comment_list[len(
                        comment_list)-1].get('rootcommentid')
                if not lasthot:
                    lasthot = comment_list[len(
                        comment_list)-1]["middlecommentcontent"][0].get("subcommentid")

                for comment in comment_list:
                    nick = comment["nick"]
                    rootcommentnick = comment.get("rootcommentnick")
                    rootcommentcontent = comment.get("rootcommentcontent")
                    comment_time = comment['time']
                    reply_content = ""
                    if comment.get("middlecommentcontent"):
                        co = comment["middlecommentcontent"]
                        for i in range(len(co)):
                            replynick = co[i]["replynick"]
                            replyednick = co[i]["replyednick"]
                            subcommentcontent = co[i]["subcommentcontent"]
                            if i == 0:
                                reply_content += f"{replynick.lstrip('@')}\n回复 {replyednick}：{subcommentcontent}"
                            else:
                                reply_content += f"// {replynick} 回复 {replyednick} ：{subcommentcontent}"
                        reply_content += f"\n\'\'\'\n{rootcommentcontent}\n\'\'\'"
                        reply_content += f"\n\t\t\t{Get.timestamp_datetime(comment_time)}"
                        comment_text = reply_content
                        Get.excelWrite(num, comment_num,
                                   label=comment_text, worksheet=worksheet)
                        comment_num += 1
                    else:
                        comment_text = f"{nick}\n{rootcommentcontent}\n\t\t\t{Get.timestamp_datetime(comment_time)}"
                        Get.excelWrite(num, comment_num,
                                   label=comment_text, worksheet=worksheet)
                        comment_num += 1

                comment_id = comment_list[-1]['commentid']
                reqtype = "2"

    workbook.save('QQSinger.xls')


def runQQSinger(song_pages=2, comment_pages=2):
    """ 爬取QQ音乐某个歌手的所有歌曲信息, 文件会保存为QQSinger.xls  """
    singer_name = input("请输入你想要爬取的歌手名：")
    print("爬取中，请耐心等待...")
    getSingerInfoAtQQ(singer_name, song_pages, comment_pages)
