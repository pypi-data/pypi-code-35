from django.db import models
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.text import Truncator
from markdown import markdown


class Category(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.SlugField(max_length=100)

    def __str__(self):  # pragma: no cover
        return self.name

    def get_absolute_url(self):
        return reverse('blog_post_list_categorised', args=[self.slug])

    class Meta:
        ordering = ('slug',)


class Tag(models.Model):
    slug = models.SlugField(max_length=100, unique=True)
    name = models.SlugField(max_length=100)

    def __str__(self):  # pragma: no cover
        return self.name

    def get_absolute_url(self):
        return reverse('blog_post_list_tagged', args=[self.slug])

    class Meta:
        ordering = ('slug',)


class Post(models.Model):
    parent = models.ForeignKey(
        'self',
        related_name='updates',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    source = models.CharField(max_length=100, db_index=True)
    remote_id = models.CharField(max_length=255, db_index=True)
    title = models.CharField(max_length=280)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True, auto_now=True)
    published = models.DateTimeField(null=True, blank=True)
    level = models.CharField(
        max_length=7,
        choices=(
            ('info', 'info'),
            ('success', 'success'),
            ('warning', 'warning'),
            ('danger', 'danger')
        ),
        default='info'
    )

    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')

    def __str__(self):  # pragma: no cover
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post_detail', args=[self.pk])

    @cached_property
    def body_html(self):
        return self.body and mark_safe(
            markdown(
                self.body,
                safe_mode=True,
                extensions=(
                    'toc',
                    'smarty',
                    'tables'
                )
            )
        ) or ''

    @cached_property
    def body_plain(self):
        return strip_tags(self.body_html)

    @cached_property
    def excerpt(self):
        stripped = self.body_plain
        truncated = Truncator(stripped).words(20)
        return mark_safe(truncated)

    class Meta:
        ordering = ('-published',)
        get_latest_by = 'published'


class CustomValue(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='custom_fields',
        on_delete=models.CASCADE
    )

    key = models.CharField(max_length=100, db_index=True)
    value = models.TextField(null=True, blank=True)
    kind = models.CharField(
        max_length=5,
        choices=(
            ('str', 'string'),
            ('bool', 'boolean'),
            ('float', 'number'),
            ('list', 'array'),
            ('dict', 'object')
        ),
        default='str'
    )

    class Meta:
        unique_together = ('post', 'key')
        ordering = ('key',)
        db_table = 'blog_post_meta'
