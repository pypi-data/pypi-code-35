from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from dmodels.models import AbstractDeactivatableModel


class Counter(AbstractDeactivatableModel):
    HEADER = 1
    BODY = 2
    ROBOTS_CHOICES = (
        (HEADER, '<head>'),
        (BODY, '<body>'),
    )
    name = models.CharField(_('Заголовок'), max_length=150)
    code = models.TextField(_('Дані'), max_length=5000, default=None)
    position = models.PositiveIntegerField(_('Позиція'), choices=ROBOTS_CHOICES, default=0, blank=True, help_text=_('для Google Analytics вибирати <head>, для більшості інших - <body>'))

    class Meta:
        verbose_name = _('Метрика')
        verbose_name_plural = _('Метрики')

    def __str__(self):
        return self.name


class MetaData(models.Model):
    ROBOTS_CHOICES = (
        models.BLANK_CHOICE_DASH[0],
        ('index, follow', 'index, follow'),
        ('index, nofollow', 'index, nofollow'),
        ('noindex, nofollow', 'noindex, nofollow'),
        ('noindex, follow', 'noindex, follow'),
    )
    title = models.CharField(_('Заголовок'), max_length=68, blank=True)
    description = models.CharField(_('Опис'), max_length=255, blank=True)
    keywords = models.CharField(_('Ключові слова'), max_length=255, blank=True)
    author = models.CharField(_('Автор'), max_length=255, blank=True)
    robots = models.CharField(_('Індексувати та переходити за посиланнями?'),
                              choices=ROBOTS_CHOICES, blank=True, max_length=20)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = _('Мета дані')
        verbose_name_plural = _('Мета дані')

    def __str__(self):
        return '{0} {1}'.format(self.content_type, self.object_id)


class StaticData(models.Model):
    name = models.CharField(_('Назва'), max_length=150)
    slug = models.CharField(_('Ссылка'), max_length=255, blank=True)
    data = models.TextField(_('Данные'), max_length=2000, blank=True)
    file = models.FileField(_('Файл'), null=True, blank=True, upload_to='files/%Y/%m/%d')

    class Meta:
        verbose_name = _('Статична сторінка чи файл')
        verbose_name_plural = _('Статичні сторінки чи файли')

    def __str__(self):
        return self.name
