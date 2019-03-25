import time
from ..utils import Get
from selenium.webdriver.common.action_chains import ActionChains


__all__ = ["runPlayNeteaseSongs", "remotePlay"]


def playANeteaseSong(music_name=None):
    ''' 播放一首网易云音乐的歌曲 '''
    if not music_name:
        music_name = input("请输入与歌曲名：")
    driver = Get(f"https://music.163.com/#/search/m/?id=768306&market=sogouqk&s={music_name}").driver
    time.sleep(2)
    driver.switch_to.frame("contentFrame")
    play = Get.locateElement(driver, "cl")("ply")
    play_time = Get.locateElement(driver, "ss")(
        ".srchsongst > div:nth-child(1) > div:nth-child(6)").text
    ActionChains(driver).click(play).perform()
    minutes, seconds = play_time.split(":")
    play_time = int(minutes) * 60 + int(seconds)
    time.sleep(play_time)
    driver.close()


def runPlayNeteaseSongs(music_name=None, music_list=None):
    ''' 播放网易云音乐的歌曲 '''
    if music_list:
        for m in music_list:
            playANeteaseSong(m)
    elif music_name:
        playANeteaseSong(music_name)
    else:
        musics = ["Merry Cristmas, Mr. Lawrence", "Viva La Vida", ]
        for m in musics:
            playANeteaseSong(m)


def remotePlay(ip_address, options=None):
    ''' 远程播放，需要服务器端安装jre和selenium standalone server '''
    if options:
        chrome_options = options
    else:
        chrome_options = Options()
        chrome_options.add_argument('--headless')
    driver = RemoteWebDriver(f"http://{ip_address}:4444/wd/hub",
                             chrome_options.to_capabilities())

    return driver
