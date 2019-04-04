import json

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout

from comk_django_plugin import general_resolve_request_data
from .BaseMoudel import BaseMoudel


class PublicServer(BaseMoudel):
    '''
    服务公共类，作为基础服务使用

    '''

    def __init__(self, request: HttpRequest):
        '''
        默认构建一个请求数据体和返回数据体

        :param request:
        '''
        super().__init__()
        self.request = request
        self.request_data = general_resolve_request_data(request)

    def return_json_response(self, data):
        '''
        传入数据，返回 JsonResponse


        :param data:
        :return:
        '''
        return JsonResponse(data)

    def return_self_json_response(self):
        '''
        使用当前服务公共类的response_data，返回 JsonResponse

        :return:
        '''
        return self.return_json_response(self.response_data)

    def return_build_success_response(self, response_data=None):
        '''
        业务成功返回，JsonResponse格式

        :param response_data:
        :return:
        '''

        return self.return_json_response(
            self.build_return_response_data('1000', data_type='1', response_data=response_data))

    def return_build_error_response(self, msg=None):
        '''
        业务失败返回，JsonResponse格式

        :param response_data:
        :return:
        '''

        return self.return_json_response(self.build_return_response_data('1000', data_type='2', msg=msg))

    def login_user(self, username, password):
        '''
        登录一个用户

        :param username:
        :param password:
        :return:
        '''
        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return True

    def logout_user(self):
        '''
        登出一个用户

        :param username:
        :param password:
        :return:
        '''
        if self.check_login_user():
            logout(self.request)

    def check_login_user(self, request=None):
        '''
        检验用户是否登录
        True 为已登录

        :param request:
        :return:
        '''
        request = request if request else self.request
        return request.user.is_authenticated()
