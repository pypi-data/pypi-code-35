# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django_szuprefix.utils import dateutils


def count_answer_user(qset=None, measures=None):
    if qset is None:
        qset = models.Answer.objects.all()
    count = lambda qset: qset.values('user').distinct().count()
    res = {}
    if isinstance(measures, (tuple, list)):
        if 'today' in measures:
            res['today'] = count(qset.filter(create_time__gte=dateutils.get_next_date(None, 0),
                                             create_time__lt=dateutils.get_next_date(None, 1)))
        if 'yesterday' in measures:
            res['yesterday'] = count(qset.filter(create_time__gte=dateutils.get_next_date(None, -1),
                                                 create_time__lt=dateutils.get_next_date(None, 0)))
        if 'all' in measures:
            res['all'] = count(qset)
    return res
