from aiconf.aiconf import fqcn


class MalformattedConfigException(Exception):
    pass


class ConfigLogicException(Exception):
    def __init__(self, cls, msg):
        super().__init__(f"{fqcn(cls)}: {msg}")
