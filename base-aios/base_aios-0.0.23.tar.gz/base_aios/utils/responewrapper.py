from base_aios.utils.returncode import ReturnCode
class ResponeResult():
    """
    返回数据：
     对象：
       data={name:aaa,age:11}
     数组：
       data = [{name:aaa, age:111},{name:bbb, age:222}]
    """
    data = {}

    """
    返回码
    """
    code = None

    """
    返回信息内容
    """
    msg = ""

    """
    返回状态，是否成功，成功：True，失败：False
    """
    status = True

    '''初始化
    
    Returns:
        [type] -- [description]
    '''

    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.data = kwargs.get("data", {})
        self.status = kwargs.get("status", True)
        self.msg = kwargs.get("msg")

    '''转成json
    
    Returns:
        [type] -- [description]
    '''

    def to_json(self):
        ret = {}
        ret["status"] = self.status
        ret["data"] = self.data
        ret["code"] = self.code
        ret["msg"] = self.msg
        ret["length"] = len(self.data) if isinstance(self.data, (list, set, dict)) else 0
        return ret

    '''
     异常信息解析
    '''

    def res_exception(self, **args):
        self.data = args.get('data', [])
        self.code = args.get('code', ReturnCode.FAILED)
        self.msg = str(args.get('msg'))
        self.status = args.get('status', False)

        return self.to_json()

    def res_success(self, **args):
        self.data = args.get('data', [])
        self.code = args.get('code', ReturnCode.SUCCESS)
        self.msg = args.get('msg', 'success')
        self.status = args.get('status', True)

        return self.to_json()

    def res_badrequest(self, **args):
        msg = args.get('msg')
        field_name = args.get('field_name')

        self.data = args.get('data', [])
        self.code = args.get('code', ReturnCode.PARAMS_ERROR)
        self.msg = msg if msg else 'required parameter \'{}\' is missing or invalidate.'.format(field_name)
        self.status = args.get('status', False)

        return self.to_json()


class ResponePageResult(ResponeResult):
    curCount = 0
    totalCount = 0
    pageNO = 0
    pageSize = 0
    totalPage = 0
    nextPage = {}
    prePage = {}

    def __init__(self, **kwargs):
        self.code = kwargs.get("code")
        self.data = kwargs.get("data")
        self.status = kwargs.get("status")
        self.msg = kwargs.get("msg")
        self.curCount = kwargs.get("curCount")
        self.totalCount = kwargs.get("totalCount")
        self.pageNO = kwargs.get("pageNO")
        self.pageSize = kwargs.get("pageSize")
        self.totalPage = kwargs.get("totalPage")

    def res_success(self, **args):

        self.data = args.get('data', [])
        self.code = args.get('code', ReturnCode.SUCCESS)
        self.msg = args.get('msg', 'success')
        self.status = args.get('status', True)

        self.curCount = args.get('curCount')
        self.totalCount = args.get('totalCount')
        self.pageNO = args.get('pageNO')
        self.pageSize = args.get('pageSize')
        self.totalPage = args.get('totalPage')

        return self.to_json()
    
    def to_json(self):
        ret = {}
        ret["status"] = self.status
        ret["data"] = self.data
        ret["code"] = self.code
        ret["msg"] = self.msg
        ret["length"] = len(self.data) if isinstance(self.data, (list, set, dict)) else 0

        ret["curCount"] = self.curCount
        ret["totalCount"] = self.totalCount
        ret["pageNO"] = self.pageNO
        ret["pageSize"] = self.pageSize
        ret["totalPage"] = self.totalPage
        return ret