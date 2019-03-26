from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Post, Tag, Category


class ContentEncodedFeed(Rss201rev2Feed):
    def root_attributes(self):
        attrs = super().root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'

        return attrs

    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        handler.addQuickElement('content:encoded', item['content_encoded'])


class PostListFeed(Feed):
    feed_type = ContentEncodedFeed

    def title(self, obj):
        return obj and obj.name or 'Notes'

    def description(self, obj):
        if isinstance(obj, Tag):
            return 'Notes tagged \'%s\'' % obj.name

        if isinstance(obj, Category):
            return 'Notes filed under \'%s\'' % obj.name

        return 'Service status updates'

    def get_object(self, request, **kwargs):
        if 'tag' in kwargs:
            return get_object_or_404(
                Tag,
                slug=kwargs['tag']
            )

        if 'category' in kwargs:
            return get_object_or_404(
                Category,
                slug=kwargs['category']
            )

    def link(self, obj):
        if isinstance(obj, Tag):
            return reverse('blog_post_list_tagged', args=[obj.slug])

        if isinstance(obj, Category):
            return reverse('blog_post_list_categorised', args=[obj.slug])

        return reverse('blog_post_list')

    def items(self, obj):
        posts = Post.objects.filter(
            parent__isnull=True,
            published__lte=timezone.now()
        )

        if isinstance(obj, Tag):
            posts = posts.filter(tags=obj)
        elif isinstance(obj, Category):
            posts = posts.filter(categories=obj)

        return posts[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body_plain

    def item_link(self, item):
        return reverse('blog_post_detail', args=[item.pk])

    def item_pubdate(self, item):
        return item.published

    def item_updateddate(self, item):
        return item.updated

    def item_categories(self, item):
        return item.categories.values_list('name', flat=True)

    def item_extra_kwargs(self, item):
        kwargs = super().item_extra_kwargs(item)
        kwargs['content_encoded'] = item.body_html

        return kwargs


class PostDetailFeed(PostListFeed):
    def title(self, obj):
        return obj.title

    def description(self, obj):
        return 'Updates on note #%d' % obj.pk

    def link(self, obj):
        return reverse('blog_post_detail', args=[obj.pk])

    def get_object(self, request, pk):
        return Post.objects.get(
            parent__isnull=True,
            pk=pk
        )

    def items(self, obj):
        return obj.updates.filter(
            published__lte=timezone.now()
        )[:10]
