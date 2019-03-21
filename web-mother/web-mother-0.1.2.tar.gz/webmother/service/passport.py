# coding:utf-8

from tweb.license import License
import config
from tweb.error_exception import ErrException, ERROR


class Passport(License):
    profiles = {
        'catalog': {
            'switches': [
                "create",
                "read",
                "update",
                "remove",
                "submit",
                "audit",
                "reject",
                "activate",
                "deactivate"
            ],
            'numbers': [
                "visible_level"  # 资源可见级别，越大表示可以看到status值更低的资源，取值范围为资源status取值范围，如0～40
            ],
        },
        'grant': {
            'switches': [
                "create",
                "read",
                "update",
                "remove"
            ]
        }
    }

    def __init__(self):
        super(Passport, self).__init__(profiles=self.profiles,
                                       authority=config.PLATFORM,
                                       secret=config.TornadoSettings['cookie_secret'])

    @staticmethod
    def add_profile(domain, profile):
        """
        :param domain:
        :param profile: 示例如下

        'catalog': {
            'switches': [
                "sample_sw1",  # 0
                "sample_sw2"
            ],

            # 共6个数值域可用
            'numbers': [
                "sample_num1",
                "sample_num2"
            ],

            # 共4个范围域可用
            'ranges': [
                "sample_range1",
                "sample_range2"
            ]
        }
        :return:
        """
        if domain in Passport.profiles:
            raise ErrException(ERROR.E50000, extra='duplicated about license profile: %s' % domain)

        Passport.profiles[domain] = profile
