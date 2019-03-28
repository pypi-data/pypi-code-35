# -*- coding:utf-8 -*- 
# author = 'denishuang'
from __future__ import unicode_literals
from . import models
from django_szuprefix.utils import dateutils, statutils
from django.db.models import Count


def count_student(qset=None, measures=None, period=None):
    qset = qset or models.Student.objects.all()
    dstat = statutils.DateStat(qset, 'create_time')
    qset_unbind = qset.filter(is_bind=False)
    funcs = {
        'today': lambda: dstat.stat("今天", only_first=True),
        'yesterday': lambda: dstat.stat("昨天", only_first=True),
        'all': lambda: qset.count(),
        'daily': lambda: dstat.stat(period),
        'unbind': lambda: qset_unbind.count(),
        'unbind_clazzs': lambda: statutils.count_by(qset_unbind, 'clazz__name', distinct=True, sort="-")
    }
    return dict([(m, funcs[m]()) for m in measures])

def count_teacher(qset=None, measures=None, period=None):
    qset = qset or models.Teacher.objects.all()
    dstat = statutils.DateStat(qset, 'create_time')
    funcs = {
        'today': lambda: dstat.stat("今天", only_first=True),
        'yesterday': lambda: dstat.stat("昨天", only_first=True),
        'all': lambda: qset.count(),
        'daily': lambda: dstat.stat(period)
    }
    return dict([(m, funcs[m]()) for m in measures])


def count_clazz(qset=None, measures=None, period=None):
    qset = qset or models.Clazz.objects.all()
    dstat = statutils.DateStat(qset, 'create_time')
    funcs = {
        'today': lambda: dstat.stat("今天", only_first=True),
        'yesterday': lambda: dstat.stat("昨天", only_first=True),
        'all': lambda: qset.count(),
        'daily': lambda: dstat.stat(period)
    }
    return dict([(m, funcs[m]()) for m in measures])
