from django.conf import settings
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Post, Category, Tag


class PostListView(ListView):
    model = Post
    paginate_by = getattr(settings, 'POSTS_PER_PAGE', 10)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            parent__isnull=True,
            published__lte=timezone.now()
        ).prefetch_related(
            'categories', 'tags'
        ).order_by('-published')

        if self.kwargs.get('tag'):
            queryset = queryset.filter(
                tags__slug=self.kwargs['tag']
            )

        if self.kwargs.get('category'):
            queryset = queryset.filter(
                categories__slug=self.kwargs['category']
            )

        return queryset

    def get_context_data(self, **kwargs):
        title_parts = kwargs.get('title_parts', [])

        kwargs['feed_title'] = 'Service status feed'
        kwargs['feed_url'] = self.request.build_absolute_uri(
            reverse('blog_post_feed')
        )

        if self.kwargs.get('tag'):
            tag = get_object_or_404(
                Tag,
                slug=self.kwargs['tag']
            )

            kwargs['tag'] = tag
            kwargs['feed_title'] = '%s tag feed' % tag.name
            kwargs['feed_url'] = self.request.build_absolute_uri(
                reverse('blog_post_feed_tagged', args=[tag.slug])
            )

            title_parts.insert(0, 'Notes tagged \'%s\'' % tag.name)

        if self.kwargs.get('category'):
            category = get_object_or_404(
                Category,
                slug=self.kwargs['category']
            )

            kwargs['category'] = category
            kwargs['feed_title'] = '%s category feed' % category.name
            kwargs['feed_url'] = self.request.build_absolute_uri(
                reverse('blog_post_feed_categorised', args=[category.slug])
            )

            title_parts.insert(0, 'Notes categorised \'%s\'' % category.name)

        kwargs['title_parts'] = title_parts
        return super().get_context_data(**kwargs)

    def get_template_names(self):
        template_names = super().get_template_names()

        if self.kwargs.get('tag'):
            template_names.insert(0, 'blog/post_list_tagged.html')

        if self.kwargs.get('category'):
            template_names.insert(0, 'blog/post_list_categorised.html')

        return template_names


class PostDetailView(DetailView):
    model = Post

    def get_queryset(self):
        return super().get_queryset().filter(
            parent__isnull=True,
            published__lte=timezone.now()
        ).prefetch_related(
            'categories', 'tags'
        )

    def get_context_data(self, **kwargs):
        kwargs['feed_title'] = 'Note #%d feed' % self.object.pk
        kwargs['feed_url'] = self.request.build_absolute_uri(
            reverse('blog_post_detail_feed', args=[self.object.pk])
        )

        return super().get_context_data(**kwargs)
