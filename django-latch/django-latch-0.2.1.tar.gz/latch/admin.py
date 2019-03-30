from django.contrib import admin
from latch.models import LatchSetup, UserProfile


class LatchSetupAdmin(admin.ModelAdmin):
    list_display = ("latch_appid", "latch_secret")

    def has_add_permission(self, request):
        return not LatchSetup.objects.exists()

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "latch_accountId")


admin.site.register(LatchSetup, LatchSetupAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
