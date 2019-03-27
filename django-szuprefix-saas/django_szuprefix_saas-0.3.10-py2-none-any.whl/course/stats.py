# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django_szuprefix.utils import dateutils
from django.db.models import Count


def count_course(qset=None, measures=None, begin_time=None):
    if qset is None:
        qset = models.Course.objects.all()
    count = lambda qset: qset.count()
    res = {}
    funcs = {
        'today': lambda: count(qset.filter(create_time__gte=dateutils.get_next_date(None, 0),
                                           create_time__lt=dateutils.get_next_date(None, 1))),
        'yesterday': lambda: count(qset.filter(create_time__gte=dateutils.get_next_date(None, -1),
                                               create_time__lt=dateutils.get_next_date(None, 0))),
        'all': lambda: count(qset),
        'daily': lambda: list(qset.filter(create_time__gt=(begin_time or dateutils.get_next_date(None, -7))).
            extra(select={'the_date': 'date(create_time)'}).
            values('the_date').
            order_by('the_date').
            annotate(number=Count('id', distinct=True)))
    }
    for m in measures:
        f = funcs[m]
        res[m] = f()
    return res
