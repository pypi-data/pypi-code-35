from django.db import models


class MetaCategory(models.Model):
    """
    Group models together.
    """

    slug = models.SlugField(max_length=50, unique=True)
    title = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title if self.title else self.slug
