#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import uuid
from logging.handlers import TimedRotatingFileHandler
import os
from collections import defaultdict
from contextlib import contextmanager
from datetime import datetime

from django.conf import settings

from m3_legacy.middleware import get_thread_data

from production_request.enums import SqlOperationEnum


def ms_from_timedelta(td):
    """
    Получает дельту, возвращает миллисекунды
    """
    return (td.seconds * 1000) + (td.microseconds / 1000.0)


@contextmanager
def calc_sql_metrics(cursor, sql):
    """
    Контекстный менеджер для подсчета времени выполнения SQL-запроса
    :param cursor: курсок к БД
    """
    start = datetime.now()

    yield

    request_uuid = getattr(
        get_thread_data(), 'production_request_uuid', None)
    if request_uuid:
        # подсчет времени выполнения sql-запроса
        if not hasattr(cursor.db, 'sql_time'):
            cursor.db.sql_time = defaultdict(float)

        duration = ms_from_timedelta(datetime.now() - start)
        cursor.db.sql_time[request_uuid] += duration

        for key, operation in SqlOperationEnum.operations_items():
            if operation in sql:
                sql_operation_attr = 'sql_{}_time'.format(key)

                if not hasattr(cursor.db, sql_operation_attr):
                    setattr(
                        cursor.db, sql_operation_attr,
                        defaultdict(type(duration))
                    )

                getattr(cursor.db, sql_operation_attr)[request_uuid] += duration

                break

        # подсчет количества sql-запросов
        if not hasattr(cursor.db, 'sql_count'):
            cursor.db.sql_count = defaultdict(int)

        cursor.db.sql_count[request_uuid] += 1

        # подсчет количества sql-операторов определенного типа
        for key, operator in SqlOperationEnum.operators_items():
            count = sql.count(operator)
            if not count:
                continue

            sql_operator_attr = 'sql_{}_count'.format(key)

            if not hasattr(cursor.db, sql_operator_attr):
                setattr(cursor.db, sql_operator_attr, defaultdict(int))

            getattr(cursor.db, sql_operator_attr)[request_uuid] += count


@contextmanager
def calc_transaction_metrics(autocommit):
    data = get_thread_data()
    request_uuid = getattr(
        get_thread_data(), 'production_request_uuid', None)
    if request_uuid:
        if not hasattr(data, 'transaction_timestamps'):
            data.transaction_timestamps = defaultdict(list)

        if not autocommit:
            data.transaction_timestamps[request_uuid].append(datetime.now())

    yield

    if request_uuid and autocommit:
        now = datetime.now()
        if not hasattr(data, 'transaction_timestamps'):
            data.transaction_timestamps = defaultdict(list)
        else:
            try:
                timestamp = data.transaction_timestamps[request_uuid].pop()
            except IndexError:
                pass
            else:
                if not hasattr(data, 'transaction_count'):
                    data.transaction_count = defaultdict(int)
                data.transaction_count[request_uuid] += 1

                if not hasattr(data, 'transaction_total'):
                    data.transaction_total = defaultdict(float)
                data.transaction_total[request_uuid] += ms_from_timedelta(
                    now - timestamp)


def get_client_ip(request):
    """
    Возвращает IP-адрес клиента, от которого пришел запрос
    """
    if hasattr(request, 'META'):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
    else:
        ip = ''

    return ip


def register_logger(
        lname, log_file=None, log_level=logging.INFO, formatter=None):
    """
    Регистрирует логгер
    """
    log_file = log_file or u'{0}.log'.format(lname)
    log_dir = settings.LOG_PATH
    log_path = os.path.join(log_dir, log_file)

    if formatter is None:
        formatter = logging.Formatter(
            "\n%(pathname)s:%(lineno)d\n[%(asctime)s] %(levelname)s: "
            "%(message)s")
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'

    l = logging.getLogger(lname)
    l.setLevel(log_level)

    # Защита от reload()
    if not l.handlers:
        handler = TimedRotatingFileHandler(
            log_path, when='D', encoding='utf-8')
        handler.setFormatter(formatter)
        l.addHandler(handler)

    return l


def to_MB(value):
    """Приводит биты в МБ"""
    return value / 1024.0 / 1024.0


class SimpleRequest(object):
    def __init__(self, path=''):
        super(SimpleRequest, self).__init__()
        self.path = path


def generate_uuid():
    return str(uuid.uuid4())[-12:]