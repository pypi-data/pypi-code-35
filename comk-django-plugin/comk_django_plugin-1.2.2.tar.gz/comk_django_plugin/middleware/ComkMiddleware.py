import datetime

from django.utils.deprecation import MiddlewareMixin

from comk_django_plugin import general_resolve_response, general_resolve_request


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
