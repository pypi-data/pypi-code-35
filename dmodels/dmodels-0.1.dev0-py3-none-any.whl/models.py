from django.db import models
from django.utils.translation import ugettext_lazy as _


class AbstractDateTrackedModel(models.Model):
    publication_date = models.DateTimeField(_('Дата Створення'), auto_now_add=True)
    modification_date = models.DateTimeField(_('Дата Модифікації'), auto_now=True)

    class Meta:
        abstract = True


class AbstractContentModel(models.Model):
    content = models.TextField(_('Контент'), blank=True)

    class Meta:
        abstract = True


class AbstractRawContentModel(models.Model):
    content = models.TextField(_('Контент'), blank=True)

    class Meta:
        abstract = True


class AbstractContentPageModel(AbstractContentModel):
    name = models.CharField(_('Тема'), max_length=150)
    slug = models.SlugField()

    title_field_name = 'name'

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractPositionedModel(models.Model):
    position = models.IntegerField(_('Позиція'), default=0, blank=True)

    class Meta:
        ordering = ['position', 'id']
        abstract = True


class DeactivatableModelQuerySet(models.QuerySet):
    def active(self):
        return self.filter(active=True)

    def disabled(self):
        return self.filter(active=False)


class AbstractDeactivatableModel(models.Model):
    active = models.BooleanField(_('Активна?'), default=True)

    objects = DeactivatableModelQuerySet.as_manager()

    class Meta:
        abstract = True


class AbstractImageModel(AbstractPositionedModel, AbstractDeactivatableModel):
    name = models.CharField(_('Назва'), max_length=150)
    file = models.ImageField(_('Зображення'), upload_to='upload_images/%Y/%m/%d/')

    class Meta(AbstractPositionedModel.Meta):
        verbose_name = _('Зображення')
        verbose_name_plural = _('Зображення')
        abstract = True

    def __str__(self):
        return self.name
