# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django_szuprefix.utils import dateutils
from django.db.models import Count
from django_szuprefix.utils import modelutils


def count_answer_user(qset=None, measures=None, begin_time=None, end_time=None):
    if qset is None:
        qset = models.Answer.objects.all()
    if begin_time:
        qset = qset.filter(create_time__gte=begin_time)
    if end_time:
        qset = qset.filter(create_time__lt=end_time)
    count = lambda qset: qset.values('user').distinct().count()
    res = {}
    funcs = {
        'today': lambda: count(qset.filter(create_time__gte=dateutils.get_next_date(None, 0),
                                           create_time__lt=dateutils.get_next_date(None, 1))),
        'yesterday': lambda: count(qset.filter(create_time__gte=dateutils.get_next_date(None, -1),
                                               create_time__lt=dateutils.get_next_date(None, 0))),
        'all': lambda: count(qset),
        'daily': lambda: modelutils.count_by(qset.extra(select={'the_date': 'date(create_time)'}), 'the_date',
                                             count_field='user_id', distinct=True),
        'clazz': lambda: modelutils.count_by(qset, 'user__as_school_student__clazz__name', count_field='user_id',
                                             distinct=True, sort="")
    }
    for m in measures:
        f = funcs[m]
        res[m] = f()
    return res
