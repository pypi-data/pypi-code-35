from .update_setting_method import UpdateSettingMethod

ALLOW_IP_LIST = []
COMK_AUTH_CODE = 'COMK_AUTH_CODE'

usm = UpdateSettingMethod()
auto_update_logsetting = usm.auto_update_logsetting
set_allow_ip_list = usm.set_allow_ip_list
set_comk_auth_code = usm.set_comk_auth_code
