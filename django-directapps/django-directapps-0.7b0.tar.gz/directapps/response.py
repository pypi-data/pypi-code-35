#
# Copyright (c) 2016, Grigoriy Kramarenko
# All rights reserved.
# This file is distributed under the same license as the current project.
#
from django.http import JsonResponse

from directapps.conf import JSON_DUMPS_PARAMS
from directapps.encoders import JSONEncoder


def make_response(data, safe=False):
    return JsonResponse(
        data,
        safe=safe,
        encoder=JSONEncoder,
        json_dumps_params=JSON_DUMPS_PARAMS,
    )
