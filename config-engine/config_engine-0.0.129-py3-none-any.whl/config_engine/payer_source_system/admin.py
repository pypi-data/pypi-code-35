from django.contrib import admin

from config_engine.payer_source_system import models


class PayerSourceSystemAdmin(admin.ModelAdmin):
    list_display = ['description', 'source_system_name', 'is_active', 'system_type', 'consumer_type', 'referrer_url',
                    'payer', 'product', ]


class CXPayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', ]


class CXProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', ]


class CXProductFeatureAdmin(admin.ModelAdmin):
    list_display = ['product', 'master_feature', 'feature', ]

admin.site.register(models.PayerSourceSystem, PayerSourceSystemAdmin)
admin.site.register(models.CXPayer, CXPayerAdmin)
admin.site.register(models.CXProduct, CXProductAdmin)
admin.site.register(models.CXProductFeature, CXProductFeatureAdmin)
