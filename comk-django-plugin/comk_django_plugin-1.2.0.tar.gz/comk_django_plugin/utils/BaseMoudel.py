class BaseMoudel():
    '''
    服务以及业务的模型基类

    '''

    def __init__(self):
        self.response_data = {'code': '8999', 'data_type': '2', 'response_data': '', 'msg': ''}

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

    def build_success_response_data(self, response_data=None):
        '''
        构建业务成功的返回数据

        :param response_data:
        :return:
        '''

        return self.build_return_response_data('1000', data_type='1', response_data=response_data)

    def build_error_response_data(self, code='1000', msg=None):
        '''
        构建业务失败的返回数据

        :param msg:
        :return:
        '''

        return self.build_return_response_data(code, data_type='2', msg=msg)
