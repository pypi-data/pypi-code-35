from django.db import models

from django.contrib.contenttypes.models import ContentType


class OverallRatingManager(models.Manager):

    def top_rated(self, model_class, cat=''):
        content_type = ContentType.objects.get_for_model(model_class)
        order_by = '-sortable_rating'

        return self.filter(
            content_type=content_type,
            category=cat,
        ).extra(
            select={
                'sortable_rating': 'COALESCE(rating, 0)',
            },
        ).order_by(order_by)
