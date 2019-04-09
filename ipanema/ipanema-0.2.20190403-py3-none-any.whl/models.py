from contextlib import contextmanager
from os import path

from peewee import Model, TextField, ForeignKeyField, DoesNotExist
from pkg_resources import resource_filename
from playhouse.sqlite_ext import SqliteDatabase

database = SqliteDatabase(None, pragmas=[
    ('foreign_keys', '1'),
    ('defer_foreign_keys', '1')
])

DEFAULT_DATABASE = resource_filename(__name__, 'languages.sqlite')


@contextmanager
def database_connection(db_path=DEFAULT_DATABASE):
    if not path.exists(db_path):
        raise OSError("db not found: %s" % db_path)

    database.init(db_path)
    database.connect()
    yield database
    database.close()


class BaseModel(Model):
    class Meta:
        database = database
        legacy_table_names = False

    @classmethod
    def sqlall(cls, safe=False):
        create_sql, _ = cls._schema._create_table(safe=safe).query()
        index_sql = [ctxt.query()[0] for ctxt in
                     cls._schema._create_indexes(safe=safe)]
        return [create_sql] + index_sql


class Family(BaseModel):
    code = TextField(unique=True, null=False)
    canonical_name = TextField(null=False)
    wikidata_item = TextField(index=True, null=True)
    family = ForeignKeyField('self', to_field='code',
                             db_column='family', null=True)

    def __str__(self):
        return self.canonical_name

    def __repr__(self):
        return repr(self.object)

    @property
    def object(self):
        return {
            'code': self.code,
            'name': self.canonical_name,
            'wikidata_item': self.wikidata_item,
            'family': str(self.family)
        }

    class Meta:
        table_name = 'families'


class Language(BaseModel):
    # order of priority/availability: ISO 639-1, 639-3, 639-2
    # https://en.wiktionary.org/wiki/Wiktionary:Languages#Language_codes
    code = TextField(unique=True, null=False)
    canonical_name = TextField(null=False, index=True)
    native_name = TextField(index=True, null=True)
    ancestor = ForeignKeyField('self', to_field='code',
                               db_column='ancestor', null=True)
    family = ForeignKeyField(Family, to_field='code',
                             db_column='family', null=True)
    character_data = TextField(null=True)
    wikidata_item = TextField(index=True, null=True)

    def __str__(self):
        return self.canonical_name

    def __repr__(self):
        return repr(self.object)

    @property
    def object(self):
        return {
            'code': self.code,
            'name': self.canonical_name,
            'native_name': self.native_name,
            'family': self.family.object if self.family else None,
            'ancestor': str(self.ancestor),
            'wikidata_item': self.wikidata_item
        }

    class Meta:
        table_name = 'languages'

    @classmethod
    def query(cls, descriptor):
        """
        :param descriptor: a language name (native or English),
                           a ISO 639-3 identifier or
                           a wikidata item id (Q...)
        :return: the language or None
        """
        try:
            return cls.get((cls.code == descriptor) |
                           (cls.canonical_name == descriptor) |
                           (cls.wikidata_item == descriptor) |
                           (cls.native_name == descriptor))
        except DoesNotExist:
            return None


class LanguageAlias(BaseModel):
    name = TextField(null=False, index=True)
    language_code = ForeignKeyField(Language, to_field='code',
                                    db_column='language_code')

    class Meta:
        table_name = 'language_aliases'


class RelativeTime(BaseModel):
    field = TextField(null=False, index=True)  # day, month, etc.
    style = TextField(null=True, index=True)   # short, narrow

    minus_two = TextField(null=True)     # day before yesterday
    minus_one = TextField(null=True)     # yesterday
    zero = TextField(null=True)          # today
    plus_one = TextField(null=True)      # tomorrow
    plus_two = TextField(null=True)      # day after tomorrow

    past_one = TextField(null=True)      # 1 day ago
    past_other = TextField(null=True)    # x days ago
    future_one = TextField(null=True)    # in 1 day
    future_other = TextField(null=True)  # in x days

    language_code = ForeignKeyField(Language,
                                    to_field='code',
                                    db_column='language_code')

    @classmethod
    def query(cls, code, field, style=None):
        """
        :param code: ISO 639-3 identifier
        :param field: minute|hour|day|week|month|quarter|year
        :param style: None|narrow|short
        :return: the relative time or None
        """
        try:
            return RelativeTime.get(
                (RelativeTime.language_code == code) &
                (RelativeTime.style == style) &
                (RelativeTime.field == field))
        except DoesNotExist:
            return None

    class Meta:
        table_name = 'relative_time'


if __name__ == '__main__':
    import peewee

    for model in peewee.sort_models([Language, Family, LanguageAlias]):
        for sql in model.sqlall():
            print(sql + ';')
