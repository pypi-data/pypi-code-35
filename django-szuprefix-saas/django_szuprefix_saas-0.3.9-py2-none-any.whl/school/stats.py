# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django_szuprefix.utils import dateutils
from django.db.models import Count

def count_student(qset=None, measures=None):
    if qset is None:
        qset = models.Student.objects.all()
    count = lambda qset: qset.count()
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



def count_teacher(qset=None, measures=None, begin_time=None):
    if qset is None:
        qset = models.Teacher.objects.all()
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



def count_clazz(qset=None, measures=None, begin_time=None):
    if qset is None:
        qset = models.Clazz.objects.all()
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