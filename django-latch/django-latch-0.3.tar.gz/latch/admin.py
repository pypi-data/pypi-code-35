from django.contrib import admin
from latch.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "latch_accountId")


admin.site.register(UserProfile, UserProfileAdmin)
