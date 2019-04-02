import json

from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login, logout


class PublicServer():
    '''
    服务公共类，作为基础服务使用

    '''

    def __init__(self, request: HttpRequest):
        '''
        默认构建一个请求数据体和返回数据体

        :param request:
        '''
        self.request = request
        self.request_data = self.make_request_data(request)
        self.response_data = {'code': '8999', 'data_type': '2', 'response_data': '', 'msg': ''}

    def make_request_data(self, request):
        request_data = dict()
        try:
            request_data.update(json.loads(self.request.body))
        except:
            pass
        request_data.update(request.GET.dict())
        request_data.update(request.POST.dict())
        return request_data

    def build_return_response_data(self, code, msg=None, response_data=None, data_type=None):
        '''
        构造返回信息

        :param code:
        :param msg:
        :return:
        '''
        self.response_data['code'] = code
        if msg:
            self.response_data['msg'] = msg
        if response_data:
            self.response_data['response_data'] = response_data
        if data_type:
            self.response_data['data_type'] = data_type
        return self.response_data

    def return_self_json_response(self):
        '''
        使用当前服务公共类的response_data，返回 JsonResponse

        :return:
        '''
        return self.return_json_response(self.response_data)

    def return_json_response(self, data):
        '''
        传入数据，返回 JsonResponse


        :param data:
        :return:
        '''
        return JsonResponse(data)

    def build_success_response_data(self, response_data=None):
        '''
        构建业务成功的返回数据

        :param response_data:
        :return:
        '''

        return self.build_return_response_data('1000', data_type='1', response_data=response_data)

    def build_error_response_data(self, msg=None):
        '''
        构建业务失败的返回数据

        :param msg:
        :return:
        '''

        return self.build_return_response_data('1000', data_type='2', msg=msg)

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
