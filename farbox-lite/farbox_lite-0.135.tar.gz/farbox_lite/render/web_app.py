#coding: utf8
from __future__ import absolute_import

# patch
from farbox_lite.template_system.monkey.patch import *

from flask import Flask
from farbox_lite.template_system.app_functions.after_request.cookie_handler import default_response_cookie_handler
from farbox_lite.template_system.app_functions.ba_request.time_cost import time_cost_handler
from farbox_lite.template_system.app_functions.before_request.basic import set_basic_vars
from farbox_lite.template_system.app_functions.utils import apply_after_request, apply_before_request

from farbox_lite.utils.error import capture_python_errors_to_local_error_log, capture_error
capture_python_errors_to_local_error_log()

from farbox_lite.render.route_view import web_route_view



app = Flask(__name__)


apply_before_request(app, time_cost_handler)
apply_after_request(app, time_cost_handler)

apply_after_request(app, default_response_cookie_handler)


apply_before_request(app, set_basic_vars)


@app.errorhandler(422)
def replace_response(error):
    # 强制 response 的替换，相当于拦截
    new_response = error.description
    return new_response

