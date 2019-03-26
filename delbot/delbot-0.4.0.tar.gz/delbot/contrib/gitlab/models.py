from datetime import timedelta
from delbot.blog.models import Post, Category, Tag
from delbot.theming.signals import sample_data_requested
from django.db import transaction
from django.dispatch import receiver
from django.utils import timezone
from django.utils.lorem_ipsum import paragraphs, words
from django.utils.text import slugify
import random


@transaction.atomic()
@receiver(sample_data_requested)
def generate_sample_data(sender, clear, **kwargs):
    now = timezone.now() - timedelta(days=1)
    levels = {
        'success': 'closed',
        'warning': 'opened'
    }

    if clear:
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Post.objects.all().delete()

    for i in range(0, 5):
        while True:
            category_name = words(
                random.choice(range(1, 4)),
                common=False
            ).capitalize()
            category_slug = slugify(category_name)

            if not Category.objects.filter(slug=category_slug).exists():
                break

        Category.objects.create(
            name=category_name,
            slug=category_slug
        )

    for i in range(0, 10):
        while True:
            tag_name = words(1, common=False).capitalize()
            tag_slug = tag_name.lower()

            if not Tag.objects.filter(slug=tag_slug).exists():
                break

        Tag.objects.create(
            name=tag_name,
            slug=tag_slug
        )

    for i in range(0, 30):
        level = random.choice(list(levels.keys()))
        post = Post.objects.create(
            source='gitlab',
            title=words(
                random.choice(range(1, 6)), common=False
            ).capitalize(),
            body='\n\n'.join(
                paragraphs(
                    random.choice(
                        range(1, 3)
                    ),
                    common=False
                )
            ),
            published=now - timedelta(
                minutes=random.choice(
                    range(0, 43829)
                )
            ),
            level=level,
            remote_id=str(
                random.choice(range(1234, 9999))
            )
        )

        for category in Category.objects.order_by('?')[
            :random.choice(range(1, Category.objects.count() + 1))
        ]:
            post.categories.add(category)

        for tag in Tag.objects.order_by('?')[
            :random.choice(range(1, 4))
        ]:
            post.tags.add(tag)

        if post.level == 'success':
            post.updates.create(
                published=post.published + timedelta(
                    minutes=random.choice(
                        range(1, 1440)
                    )
                ),
                title='Status set to %s' % levels[level]
            )

            post.updated = now
            post.save()
