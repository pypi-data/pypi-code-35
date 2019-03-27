from django.db import models
from uuid import uuid4
import logging
import traceback

# Create your models here.
class LogRecord(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    funcname = models.CharField(max_length=255)
    modulename = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    logger = models.CharField(max_length=255)
    level = models.IntegerField()
    trace = models.CharField(max_length=1024)
    msg = models.CharField(max_length=1024)

    class Meta:
        verbose_name = "LogRecord"
        verbose_name_plural = "LogRecords"
        ordering = ("id", "-created_at")

    def __str__(self):
        return "<LogRecord: %d - %s %s>" % (
            self.id,
            self.created_at.strftime("%m/%d/%Y-%H:%M:%S"),
            self.msg[:50],
        )
