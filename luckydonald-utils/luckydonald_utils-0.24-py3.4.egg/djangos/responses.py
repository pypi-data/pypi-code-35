# -*- coding: utf-8 -*-
__author__ = 'luckydonald'

from luckydonaldUtils.logger import logging  # pip install luckydonald-utils
logger = logging.getLogger(__name__)
from django.http import JsonResponse

def json_return(status=None, statusText=None, exception=None, content=None):
	msg = {"status": 200, "statusText": "OK"}
	if isinstance(exception, Exception):
		logger.warn("Json Exception")
		msg["status"] = 500
		msg["statusText"] = "INTERNAL SERVER ERROR"
		msg["content"] = "Generic Error"
		if settings.DEBUG:
			msg["exception"] = str(exception)
		#end if
	#end if
	if status:
		msg["status"] = status
	if statusText:
		msg["statusText"] = statusText
	if content:
		msg["content"] = content
	#end if
	return JsonResponse(msg, msg["status"])