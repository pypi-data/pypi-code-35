try:
    from modeltranslation.admin import TranslationAdmin

    class CustomTabbedTranslationAdmin(TranslationAdmin):
        class Media:
            js = (
                'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
                'js/tabbed_translation_fields_extended.js',
            )
            css = {
                'screen': (
                    'modeltranslation/css/tabbed_translation_fields.css',
                    'css/tabbed_translation_fields_extended.css'
                ),
            }
except ImportError:
    pass




