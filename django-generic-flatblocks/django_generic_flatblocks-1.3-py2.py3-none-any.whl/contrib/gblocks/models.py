from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


@python_2_unicode_compatible
class Title(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=True)

    def __str__(self):
        return "(TitleBlock) %s" % self.title


@python_2_unicode_compatible
class Text(models.Model):
    text = models.TextField(_('text'), blank=True)

    def __str__(self):
        return "(TextBlock) %s..." % self.text[:20]


@python_2_unicode_compatible
class Image(models.Model):
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=True)

    def __str__(self):
        return "(ImageBlock) %s" % self.image


@python_2_unicode_compatible
class TitleAndText(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=True)
    text = models.TextField(_('text'), blank=True)

    def __str__(self):
        return "(TitleAndTextBlock) %s" % self.title


@python_2_unicode_compatible
class TitleTextAndImage(models.Model):
    title = models.CharField(_('title'), max_length=255, blank=True)
    text = models.TextField(_('text'), blank=True)
    image = models.ImageField(_('image'), upload_to='gblocks/', blank=True)

    def __str__(self):
        return "(TitleTextAndImageBlock) %s" % self.title
