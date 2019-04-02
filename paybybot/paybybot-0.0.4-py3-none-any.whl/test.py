from paybybot import *
from paybybot.bot import *

task = config.get_config()[0]
pbp_login = task["paybyphone"]["login"]
pbp_pwd = task["paybyphone"]["password"]

bot = Bot("firefox")
connected = bot.connect(pbp_login, pbp_pwd)
plate = task["plate"]
location = task["pay"]["location"]
rate = task["pay"]["rate"]
duration = task["pay"]["duration"]
check_cost = task["pay"].get("check-cost")

bot.pay(
    plate=task["plate"],
    location=task["pay"]["location"],
    rate=task["pay"]["rate"],
    duration=task["pay"]["duration"],
    check_cost=task["pay"].get("check-cost"),
)


self = bot
self.driver.get(self.PARK_URL)

# select vehicle
selected, *choices = [
    e.get_attribute("innerHTML")
    for e in self.driver.find_elements_by_class_name("option-label")
]

idx_selected = choices.index(selected)
idx_target = choices.index(plate)
delta = idx_target - idx_selected

self.send_keys(Keys.TAB)
sleep(0.5)
self.send_keys(Keys.TAB)
sleep(0.5)

if delta:
    self.send_keys(Keys.SPACE)
    sleep(0.5)
    for i in range(-delta):
        self.send_keys(Keys.UP)
    for i in range(delta):
        self.send_keys(Keys.DOWN)
    sleep(0.5)
    self.send_keys(Keys.SPACE)

self.send_keys(Keys.TAB)
sleep(0.5)

