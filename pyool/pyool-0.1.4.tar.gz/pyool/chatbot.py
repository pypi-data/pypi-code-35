import requests 
import time 
from .logger_setting import logger  



# Defining ChatBot specific Class to send messages to Dingtalk 

class ChatBot: 

    def send_markdown(self, payload, access_token, retry_time = 3, buffering = 5): 
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + str(access_token)  
        headers = {"Content-Type": "application/json;charset=utf-8"}

        attempt = 0 

        while attempt <= retry_time: 
            logger.info("Sending to Dingtalk .....")

            r = requests.post(url, headers = headers, json = payload) 

            if (r.text == """{"errcode":0,"errmsg":"ok"}""" or r.text == """{"errmsg":"ok","errcode":0}"""): 
                logger.info("Message is sent.")
                break 

            else: 
                attempt += 1
                logger.error("Attempt {}, error {}. Retrying .....".format(attempt, r.text)) 
                time.sleep(buffering)
                continue 
            
            raise RuntimeError("Cannnot send message due to %s" % r.text) 


    def send2ding(self, title, message, access_token, retry_time = 3, buffering = 5):
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": message 
            }, 
            "at": {}
        }

        self.send_markdown(payload = payload, access_token = access_token, retry_time = retry_time, buffering = buffering) 
