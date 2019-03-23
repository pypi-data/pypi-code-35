from ..utils import Get
import re


__all__ = ["queryChineseWeather", "runSendCityWeatherEveryDay"]


def queryChineseWeather(city_name="广州"):
    ''' 在中国天气网查询天气 '''
    while True:
        if not city_name:
            city_name = input("请问要查询哪里的天气：")
        city_url = f"http://toy1.weather.com.cn/search?cityname={Get.urlencode(city_name)}"
        city_json = Get.urllibOpenJson(city_url)

        if city_json:
            if city_json[0].get("ref"):
                city_string = city_json[0]["ref"]
                city_code = re.findall("\d+", city_string)[0]
        else:
            print("城市地址输入有误，请重新输入！")
            city_name = ""
            continue

        weather_url = f"http://www.weather.com.cn/weather1d/{city_code}.shtml"
        weather_soup = Get.urllibOpenSoup(weather_url)
        weather = weather_soup.find(
            "input", id="hidden_title").get("value").split()

        return weather


def runSendCityWeatherEveryDay(city="北京"):
    ''' 每天定时发送天气信息到指定邮箱 '''
    recipients, account, password, subj, text = Get.mailSendInput()
    weather = queryChineseWeather(city)
    text = " ".join(weather)
    daytime = input("请问每天的几点发送邮件？格式'18:30'，不包含单引号 ：")

    Get.scheduleFuncEveryDayTime(Get.mailSend, daytime, recipients, account,
                            password, subj, text)
