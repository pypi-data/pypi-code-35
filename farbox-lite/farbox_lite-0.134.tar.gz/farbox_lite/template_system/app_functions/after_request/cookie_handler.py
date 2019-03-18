# coding: utf8
import time
from flask import g, request


def set_cookies(response):
    # the value must dumps by singer
    # 在website.core中调用，after_request，可以处理安全性cookie的读写删除
    cookies_to_set = getattr(g, 'cookies', {})
    for k, v in cookies_to_set.items():
        # 用expires, 而非max_age，这样可以重复set_cookie, 即使nano在proxy的情况下
        response.set_cookie(k, v, expires=time.time()+10*60)

    # delete the cookies
    cookies_to_delete = getattr(g, 'cookies_to_delete', [])
    for key in cookies_to_delete:
        if key not in cookies_to_set and key in request.cookies:
            response.delete_cookie(key)


def default_response_cookie_handler(response):
    set_cookies(response)

    if getattr(g, 'response_content_type', None):
        response.content_type = g.response_content_type

    return response
