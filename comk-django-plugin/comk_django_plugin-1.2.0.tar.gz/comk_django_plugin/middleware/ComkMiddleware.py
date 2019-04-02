import datetime
import json

from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class ComkMiddleware(MiddlewareMixin):
    '''
    个人中间件

    '''

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.start_time = None  # 程序开始运行时间
        self.end_time = None  # 程序结束运行时间

    def __call__(self, request):
        return super().__call__(request)

    def process_request(self, request):
        self.start_time = datetime.datetime.now()  # 程序开始运行时间
        return None

    # def process_view(self, request, view_func, view_args, view_kwargs):
    #     pass

    # def process_template_response(self, request, response):
    #     return response

    # def process_exception(self, request, exception):
    #     pass

    def process_response(self, request, response):
        self.end_time = datetime.datetime.now()  # 程序结束运行时间
        return response

    def resolve_request(self, request):
        '''
        解析 request 数据

        :param request:
        :return:
        '''
        return_L = []
        # print(request.META.get('HTTP_X_REAL_IP'))
        # print(request.META)
        return_L.append(request.META.get('REMOTE_ADDR'))
        return_L.append(request.scheme)
        return_L.append(request.get_host())
        return_L.append(request.path)
        return_L.append(request.method)
        method = request.method
        data = {}
        if method == 'GET':
            data = request.GET.dict()
        elif method == 'POST':
            data = request.POST.dict()
            if not data:
                body = request.body
                if body:
                    try:
                        data = json.loads(body)
                    except:
                        data = body

        return_L.append(str(data))
        return ' '.join(return_L)

    def resolve_response(self, response):
        '''
        解析 response 数据

        :param response:
        :return:
        '''
        return_L = []

        status_code = str(response.status_code)
        return_L.append(status_code)

        data = {}

        if status_code.startswith('2'):
            if isinstance(response, JsonResponse):
                data = json.loads(response.content)
            # elif isinstance(response, HttpResponse):
            #     data = response.content.decode('utf-8')
        return_L.append(str(data))
        return ' '.join(return_L)
