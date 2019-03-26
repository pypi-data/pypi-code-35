import datetime
import logging
import re

from django.http import HttpResponse

logger = logging.getLogger(__name__)


def get_current_datetime():
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


def camel_to_snake(camel_name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', camel_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
