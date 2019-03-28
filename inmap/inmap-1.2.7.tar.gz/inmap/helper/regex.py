import re


class RegexHelper:

    port = "[0-9]{1,}\/[a-z]{1,3}"
    state = ""
    service = ""
    version = ""
    ip_address  = "([0-9]{1,3}\.){3}[0-9]{0,3}"
    mac_address = "([0-9|a-f]{2}:){5}[0-9|a-f]{2}"
    device_type = ""

    @staticmethod
    def check_mac_address(str_arg):
        return True if re.search(RegexHelper.mac_address, str_arg, re.IGNORECASE) else False

    @staticmethod
    def check_ip_address(str_arg):
        return True if re.search(RegexHelper.ip_address, str_arg) else False

    @staticmethod
    def check_port_prot(str_arg):
        return True if re.search(RegexHelper.port, str_arg, re.IGNORECASE) else False

    @staticmethod
    def get_mac_address(str_arg):
        match = re.search(RegexHelper.mac_address, str_arg, re.IGNORECASE)
        if match:
            return match[0]

        return 0

    @staticmethod
    def get_ip_address(str_arg):
        match = re.search(RegexHelper.ip_address, str_arg, re.IGNORECASE)
        if match:
            return match[0]

        return 0
