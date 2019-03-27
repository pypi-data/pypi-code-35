from django.contrib import admin
from django.utils.html import format_html

from db_loghandler.models import LogRecord
import logging

# Register your models here.
class LogRecordAdmin(admin.ModelAdmin):
    list_display = ("message", "traceback", "created_datetime")
    list_filter = ("level", "logger")
    list_per_page = 10

    def message(self, instance):
        return format_html("<span>{msg}</span>", msg=instance.msg)

    message.short_description = "Message"

    def traceback(self, instance):
        return format_html(
            "<pre><code>{content}</code></pre>",
            content=instance.trace if instance.trace else "",
        )

    def created_datetime(self, instance):
        return instance.created_at.strftime("%Y-%m-%d %X")

    created_datetime.short_description = "Created Datetime"


admin.site.register(LogRecord, LogRecordAdmin)
