from datetime import datetime

from peewee import CharField, DateTimeField, Model, Proxy
from playhouse.postgres_ext import JSONField

db = Proxy()


class ModelBase(Model):
    _ns = CharField(max_length=16, index=True)
    created_on = DateTimeField(default=datetime.utcnow)


class ModuleSetting(ModelBase):
    module = CharField(max_length=256)
    settings = JSONField(null=True)

    def json(self):
        return self.settings

    class Meta:
        database = db
        table_name = 'settings_module_settings'
        indexes = (
            (('_ns', 'module'), True),
        )
