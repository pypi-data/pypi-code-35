from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Thread(models.Model):
    title = models.TextField()
    text = models.TextField(null=True)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    dateCreated = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = (
            ('view_thread', 'Read'),
            ('control_thread', 'Control'),
        )
        auto_author = 'author_user'
        ordering = ['-dateCreated']

    def __str__(self):
        return '{}'.format(self.title)


class Message(models.Model):
    dateCreated = models.DateField(auto_now_add=True)
    text = models.TextField()
    thread = models.ForeignKey("Thread", on_delete=models.DO_NOTHING)
    author_user = models.ForeignKey(settings.AUTH_USER_MODEL)
    # response_to = models.ForeignKey(Member, on_delete=models.SET_NULL, related_name="response", blank=True, null=True)

    class Meta:
        permissions = (
            ('view_message', 'Read'),
            ('control_message', 'Control'),
        )
        auto_author = 'author_user'
        ordering = ['dateCreated']

    def __str__(self):
        return '{}, le {}'.format(self.text, self.dateCreated)