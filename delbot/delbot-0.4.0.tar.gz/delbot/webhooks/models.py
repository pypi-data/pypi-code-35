from django.db import models


class Header(models.Model):
    name = models.CharField(max_length=100)
    value = models.TextField(null=True, blank=True)

    def __str__(self):  # pragma: no cover
        return self.name


class Request(models.Model):
    sent = models.DateTimeField(auto_now_add=True)
    handler = models.CharField(max_length=100)
    request_uri = models.URLField(max_length=512)
    request_method = models.CharField(max_length=10)
    request_body = models.TextField(null=True, blank=True)
    request_headers = models.ManyToManyField(
        Header,
        related_name='requested'
    )

    response_code = models.IntegerField()
    response_body = models.TextField(null=True, blank=True)
    response_headers = models.ManyToManyField(
        Header,
        related_name='responded'
    )

    def __str__(self):  # pragma: no cover
        return self.request_uri

    class Meta:
        ordering = ('-sent',)
