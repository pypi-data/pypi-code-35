from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Interaction)
admin.site.register(models.OverallRating)
admin.site.register(models.Rating)
admin.site.register(models.SkipRating)
