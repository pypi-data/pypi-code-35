"""
针对FD的一些操作
"""
import requests
from munch import Munch

from api.exceptions import ServiceInnerException, IllegalArgumentException, AuthException
from client import check_instance_avaliable, do_service


def fd(fd_code):
    """
    获取某一个FD对象
    :param fd_code: fd的唯一code
    :return: FD对象
    """
    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/{fd_code}")

        if r is not None:
            return Munch(r)
        else:
            return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def size(fd_code):
    """
    获取数据的条数
    :param fd_code:  fd的唯一code
    :return: 数据的条数 没得就返回0
    """
    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/{fd_code}/size")

        if  r is not None:
            return r
        else:
            return 0
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def is_empty(fd_code):
    """
    判断数据集是否为空
    :param fd_code: fd的唯一code
    :return: 如果为空返回True,否则返回False
    """
    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/{fd_code}/empty")

        if r is not None:
            return r
        else:
            return True
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def collect(fd_code):
    """
    返回整个数据集
    :param fd_code: fd的唯一code
    :return:
    """
    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/{fd_code}/all")
        if r is not None:
            if isinstance(r, list):
                return [Munch(x) for x in r]
            else:
                return Munch(r)
        else:
            return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def query(fd_code, query_str, parameters={}):
    """
    对数据集进行查询
    :param fd_code: fd的唯一code
    :param query_str: 查询语句
    :param parameters: 查询可能涉及的参数 K/V形式
    :return:
    """
    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/{fd_code}/query",method="post",data=parameters,params={'query': query_str})

        if  r is not None:
            if isinstance(r, list):
                return [Munch(x) for x in r]
            else:
                return Munch(r)
        else:
            return None
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


# region saveOrUpdate  现在是直接拷的代码,后面重构
def add_datas(fd_code, result_list):
    """
    增加数据
    :param fd_code: fd的唯一code
    :param result_list: 要被写入的数据 是一个List
    :return:
    """
    if result_list is None:
        return

    if not isinstance(result_list, list):
        raise IllegalArgumentException("输入的参数:result_list 不是数组")

    check_instance_avaliable()

    request = []
    for result in result_list:
        if not isinstance(result, Munch):
            # 说明不是 Munch类型的 判断是否是Dict的
            if isinstance(result, dict):
                # 如果是dict类型的,直接发
                request.append(result)
        else:
            # 说明是munch的,那么就转成Dict的
            request.append(result.toDict())

    try:
        r = do_service(f"/remote/fd-service/{fd_code}", method="post", data=request,return_type="None")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code < 500:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def update_datas(fd_code, result_list):
    """
    更新数据
    :param fd_code: fd的唯一code
    :param result_list: 要被更新的数据 是一个List
    :return:
    """
    if result_list is None:
        return

    if not isinstance(result_list, list):
        raise IllegalArgumentException("输入的参数:result_list 不是数组")

    check_instance_avaliable()

    request = []
    for result in result_list:
        if not isinstance(result, Munch):
            # 说明不是 Munch类型的 判断是否是Dict的
            if isinstance(result, dict):
                # 如果是dict类型的,直接发
                request.append(result)
        else:
            # 说明是munch的,那么就转成Dict的
            request.append(result.toDict())

    try:
        r = do_service(f"/remote/fd-service/{fd_code}", method="put", data=request, return_type="None")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code < 500:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def save_or_update_datas(fd_code, result_list):
    """
    新增或更新数据
    :param fd_code:  fd的唯一code
    :param result_list: upsertCache
    :return:
    """
    if result_list is None:
        return

    if not isinstance(result_list, list):
        raise IllegalArgumentException("输入的参数:result_list 不是数组")

    check_instance_avaliable()

    request = []
    for result in result_list:
        if not isinstance(result, Munch):
            # 说明不是 Munch类型的 判断是否是Dict的
            if isinstance(result, dict):
                # 如果是dict类型的,直接发
                request.append(result)
        else:
            # 说明是munch的,那么就转成Dict的
            request.append(result.toDict())

    try:
        r = do_service(f"/remote/fd-service/{fd_code}/upsert", method="post", data=request, return_type="None")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


# endregion


def delete_all(fd_code):
    """
    删除数据集中所有数据
    :param fd_code: fd的唯一code
    :return:
    """
    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/{fd_code}", method="delete", return_type="None")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def delete_query(fd_code, query_str):
    """
    删除数据集中查询语句命中的数据
    :param fd_code: fd的唯一code
    :param query_str: 查询语句
    :return:
    """
    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/{fd_code}", method="delete",params={'query': query_str}, return_type="None")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e


def exists_fds(fds):
    """
    判断fd是否存在
    :param fds:
    :return:
    """
    if fds is None:
        return False

    if not isinstance(fds, list):
        raise IllegalArgumentException("检测fd是否存在失败,输入参数不是一个list")

    check_instance_avaliable()

    try:
        r = do_service(f"/remote/fd-service/exists", method="post", data=fds)
        if r is not None:
            return r
        else:
            return False
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            # 说明服务器端报错了
            raise ServiceInnerException(e.response._content.decode('utf-8'))
        elif e.response.status_code >= 400 and e.response.status_code<500 and e.response.status_code!=404:
            # 说明是认证相关的错误
            raise AuthException(f"服务端异常 {str(e)} {e.response._content.decode('utf-8')}")
        raise e
