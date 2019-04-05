from django.contrib import admin

from datawok.models import Meta, MetaCategory, Query, datawok_models

for model in datawok_models:
    admin.site.register(model)

admin.site.register(Meta)
admin.site.register(MetaCategory)
admin.site.register(Query)
