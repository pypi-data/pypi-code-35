import logging
import sys

from django.views.debug import technical_500_response

from comk_django_plugin import ALLOW_IP_LIST, COMK_AUTH_CODE
from comk_django_plugin.middleware import ComkMiddleware


class RequestLogMiddleware(ComkMiddleware):
    '''
    请求中间件（记录请求、返回与错误信息）

    '''

    def process_exception(self, request, exception):
        '''
        对异常进行记录

        :param request:
        :param exception:
        :return:
        '''
        request_result = self.resolve_request(request)
        log = logging.getLogger('comk_exception_log')  # 加载记录器
        log.exception(request_result)

        remote_addr = request.META.get('REMOTE_ADDR')
        comk_auth_code = request.GET.get('comk_auth_code')

        if request.user.is_superuser or remote_addr in ALLOW_IP_LIST or comk_auth_code == COMK_AUTH_CODE:
            # 即使在生产环境下，也允许查看具体的报错信息的方法
            return technical_500_response(request, *sys.exc_info())

    def process_response(self, request, response):
        '''
        对返回进行记录

        :param request:
        :param response:
        :return:
        '''
        super().process_response(request, response)
        request_result = self.resolve_request(request)
        response_result = self.resolve_response(response)
        run_time = (self.end_time - self.start_time).total_seconds()
        log = logging.getLogger('comk_request_log')  # 加载记录器
        log.info(request_result + ' ' + response_result + ' ' + str(run_time))
        return response
