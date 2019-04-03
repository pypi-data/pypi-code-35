from datetime import datetime

from peewee import (BooleanField, CharField, DateTimeField, Model, Proxy,
                    TextField)

db = Proxy()


class ModelBase(Model):
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    deleted_at = DateTimeField(null=True, index=True)

    def del_inst(self):
        self.deleted_at = datetime.utcnow()
        self.save()

    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        super(ModelBase, self).save(*args, **kwargs)

    @classmethod
    def sel(cls):
        return cls.select().where(cls.deleted_at == None)  # noqa: E711


class Namespace(ModelBase):
    uid = CharField(max_length=32, unique=True)
    name = CharField(max_length=64)
    description = TextField(null=True)
    is_active = BooleanField(default=False)
    _ns = CharField(max_length=32)

    def json(self):
        return {
            '_id': self.uid,
            'name': self.name,
            'description': self.description
        }

    class Meta:
        database = db
        table_name = 'ns_namespaces'
