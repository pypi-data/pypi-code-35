import json

from django.http import JsonResponse


def general_resolve_request_data(request):
    '''
    解析 request 的请求数据为 dict

    :param request:
    :return:
    '''
    request_data = dict()
    try:
        request_data.update(json.loads(request.body))
    except:
        pass
    request_data.update(request.GET.dict())
    request_data.update(request.POST.dict())
    return request_data


def general_resolve_request(request):
    '''
    解析 request 的所有参数为 str

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

    if request.user.is_authenticated():
        user_key = str(request.user.pk)
    else:
        user_key = 'AnyUser'
    return_L.append(user_key)

    return_L.append(str(general_resolve_request_data(request)))
    return ' -- '.join(return_L)


def general_resolve_response(response):
    '''
    解析 response 的所有参数为 str

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
    return ' -- '.join(return_L)
