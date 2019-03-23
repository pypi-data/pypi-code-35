from collections import defaultdict
from django.contrib.postgres.fields import JSONField
from psycopg2.extras import Json


__all__ = ['TranslationField']


class Translations(object):

    def __init__(self, value=None):
        self.data = value if value is not None else defaultdict(dict)

    def __str__(self):
        return str(self.data)

    def set_for(self, key, language, value):
        self.data[language][key] = value

    def get_for(self, key, language):
        return self.data[language].get(key)

    def clear(self):
        self.data = defaultdict(dict)


class TranslationField(JSONField):

    def __init__(self, verbose_name=None, name=None, **kwargs):
        kwargs['default'] = Translations
        return super(TranslationField, self).__init__(verbose_name, name, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(TranslationField, self).deconstruct()
        del kwargs['default']
        return name, path, args, kwargs

    def to_python(self, value):
        return Translations(value)

    def from_db_value(self, value, expression, connection, context):
        return Translations(value)

    def get_prep_value(self, value):
        return super(TranslationField, self).get_prep_value(value.data)

    def get_prep_lookup(self, lookup_type, value):
        if lookup_type in ('has_key', 'has_keys', 'has_any_keys'):
            return value
        if isinstance(value, (dict, list)):
            return Json(value)
        return super(JSONField, self).get_prep_lookup(lookup_type, Translations(value))

    def validate(self, value, model_instance):
        return super(TranslationField, self).validate(value.data, model_instance)
