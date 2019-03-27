from modeltranslation.translator import translator, TranslationOptions
from .models import MetaData


class MetaDataTranslationOptions(TranslationOptions):
    fields = 'title', 'keywords', 'description', 'author'


translator.register(MetaData, MetaDataTranslationOptions)
