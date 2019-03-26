from django.contrib import admin

from config_engine.semantic_key_registry import models


class CXSemanticEventKeyAdmin(admin.ModelAdmin):
    list_display = ['semantic_key', 'display_name', 'description', 'why_captured', 'feature', 'is_primary_feature_key',
                    'event_object', 'event_action', ]

admin.site.register(models.CXSemanticEventKey, CXSemanticEventKeyAdmin)
