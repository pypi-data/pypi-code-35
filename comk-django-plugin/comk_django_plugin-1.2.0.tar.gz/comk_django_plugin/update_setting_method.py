import comk_django_plugin
from comk_django_plugin.logsetting.comk_setting import LOGGING as comk_logsetting


class UpdateSettingMethod():
    '''
    更新django_setting的类

    '''

    def auto_update_logsetting(self, django_logsetting=None):
        '''
        合并日志配置，目的是添加本模块所需要的日志配置

        :param django_logsetting:
        :return:
        '''
        if django_logsetting and isinstance(django_logsetting, dict):
            return self.merge_dicts(django_logsetting, comk_logsetting)
        else:
            return comk_logsetting

    def merge_dicts(self, dict_one: dict, dict_two: dict):
        '''
        深度合并两个dict

        :param dict_one:
        :param dict_two:
        :return:
        '''
        one_keys = dict_one.keys()
        tow_keys = dict_two.keys()
        for tow_key in tow_keys:
            if tow_key in one_keys:
                one_value = dict_one.get(tow_key)
                two_value = dict_two.get(tow_key)
                if isinstance(one_value, dict) and isinstance(two_value, dict):
                    self.merge_dicts(one_value, two_value)
            else:
                dict_one[tow_key] = dict_two.get(tow_key)
        return dict_one

    def set_allow_ip_list(self, allow_ip_list):
        '''
        更改允许查看报错信息的ip

        :param allow_ip_list:
        :return:
        '''
        if isinstance(allow_ip_list, (list, tuple)):
            comk_django_plugin.ALLOW_IP_LIST = allow_ip_list
        else:
            raise Exception('allow_ip_list must be list or tuple')

    def set_comk_auth_code(self, comk_auth_code):
        '''
        更改允许查看报错信息的code

        :param allow_ip_list:
        :return:
        '''
        if isinstance(comk_auth_code, str):
            comk_django_plugin.COMK_AUTH_CODE = comk_auth_code
        else:
            raise Exception('comk_auth_code must be str')
