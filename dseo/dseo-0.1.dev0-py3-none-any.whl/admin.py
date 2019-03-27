from django.contrib import admin

from .models import MetaData, StaticData, Counter

try:
    from modeltranslation.admin import TranslationGenericStackedInline as GenericStackedInline
except ImportError:
    from django.contrib.contenttypes.admin import GenericStackedInline


class MetaDataInline(GenericStackedInline):
    model = MetaData
    max_num = 1
    suit_classes = 'suit-tab suit-tab-meta'


@admin.register(StaticData)
class StaticDataAdmin(admin.ModelAdmin):
    model = StaticData
    list_display = ['name', 'slug', 'data', 'file']


@admin.register(Counter)
class CounterAdmin(admin.ModelAdmin):
    model = StaticData
    list_display = ['name', 'code', 'position']
