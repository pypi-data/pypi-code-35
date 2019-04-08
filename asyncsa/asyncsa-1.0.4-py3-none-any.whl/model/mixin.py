from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declared_attr


class Mixin:

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def instancefy(cls, result=None):
        if isinstance(result, list):
            result = [cls(**item) for item in result]
        else:
            result = cls(**result)
        return result

    async def save(self):
        await self.manager().instance(
            self, model=self.__class__, q_type='update')
        return self

    @classmethod
    async def create(cls, **kwargs):
        instance = cls(**kwargs)
        await cls.manager().instance(
            instance, model=cls, q_type='add')
        result = await cls.get(**kwargs)
        return result[-1]

    @classmethod
    async def get(cls, **kwargs):
        result = await cls.manager().get_by_param(params=kwargs, model=cls)
        return cls.instancefy(result)

    async def delete(self, *args, **kwargs):
        await self.manager().instance(
            self, model=self.__class__, q_type='delete')
        return self.id or self.pk

    @classmethod
    async def all(cls):
        result = await cls.manager().all(model=cls)
        return cls.instancefy(result)

    @classmethod
    async def create_table(cls, Force=False):
        result = await cls.manager().create_table(model=cls, Force=Force)
        return result

    @classmethod
    def objects(cls, columns=None):
        if columns and isinstance(columns, list):
            return select(columns)
        else:
            return select([cls])

    @classmethod
    def manager(cls):
        if not cls._manager:
            raise Exception('model manager muset be set:_manager')
        return cls._manager
