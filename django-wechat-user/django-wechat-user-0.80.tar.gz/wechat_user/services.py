import base64
import json
import logging

import requests
from Crypto.Cipher import AES
from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from rest_framework.exceptions import APIException

from .models import *

# logger
logger = logging.getLogger(__name__)


def exchange_access_token(code):
    url = f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={settings.WECHAT_APPID}&secret={settings.WECHAT_APPSECRET}&code={code}&grant_type=authorization_code"

    # send request
    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    # check error
    if "errcode" in data:
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)
    return data["openid"], data["access_token"], data["refresh_token"], data["expire_in"]


def fetch_user_info(access_token, openid):
    url = f"https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}&lang=zh_CN"
    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    # check error
    if "errcode" in data:
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)
    return data


def exchange_session_key(code):
    url = f"https://api.weixin.qq.com/sns/jscode2session?appid={settings.WECHAT_APPID}&secret={settings.WECHAT_APPSECRET}&js_code={code}&grant_type=authorization_code"

    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    if "errcode" in data and data["errcode"] != 0:
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)
    return data["openid"], data["session_key"], data.get("unionid", None)


def unpad(s):
    return s[: -ord(s[len(s) - 1 :])]


def decrypt_user_info(session_key, encryptedData, iv):
    cipher = AES.new(base64.b64decode(session_key), AES.MODE_CBC, base64.b64decode(iv))
    decrypted = json.loads(unpad(cipher.decrypt(base64.b64decode(encryptedData))))
    if decrypted["watermark"]["appid"] != settings.WECHAT_APPID:
        raise Exception("Invalid Buffer")
    return decrypted


def get_server_access_token():
    access_token = cache.get("server:access_token")
    if access_token:
        return access_token

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={settings.WECHAT_APPID}&secret={settings.WECHAT_APPSECRET}"
    response = requests.get(url)
    response.encoding = "utf-8"
    data = response.json()
    if "errcode" in data and data["errcode"] != 0:
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)
    cache.set("server:access_token", data["access_token"], data["expires_in"] - 900)
    return data["access_token"]


def get_wxa_code_for_user(user):
    """
    """
    access_token = get_server_access_token()

    url = f"https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={access_token}"

    data = {"scene": f"userid#{user.id}"}
    response = requests.post(url, json=data)

    if response.headers["Content-Type"] != "image/jpeg":
        data = response.json()
        error_msg = "{}({})".format(data["errmsg"], data["errcode"])
        logger.error(error_msg)
        raise APIException(error_msg)

    wxacode, is_created = UserWxaCode.objects.get_or_create(owner=user)
    wxacode.image.save(f"wxacode_{user.id}.jpg", ContentFile(response.content))
    wxacode.save()
    return wxacode
