from rest_framework import serializers

from .fields import Translations


class TranslationField(serializers.Field):

    def to_representation(self, obj):
        return obj.data

    def to_internal_value(self, data):
        return Translations(data)
