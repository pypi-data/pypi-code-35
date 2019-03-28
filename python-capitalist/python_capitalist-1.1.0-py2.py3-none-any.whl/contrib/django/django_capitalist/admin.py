from django.contrib import admin

from .models import Account, Currency


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass
