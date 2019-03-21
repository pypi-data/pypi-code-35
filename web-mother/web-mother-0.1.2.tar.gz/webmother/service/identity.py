# coding:utf-8

from tweb.license import License
import config


class Identity(License):
    profiles = {
        'org': {
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
        'member': {
            'switches': [
                "create",
                "read",
                "update",
                "remove"
            ]
        },
        'app': {
            'switches': [
                "create",
                "remove"
            ]
        }
    }

    def __init__(self):
        super(Identity, self).__init__(profiles=self.profiles,
                                       authority=config.PLATFORM,
                                       secret=config.TornadoSettings['cookie_secret'])
