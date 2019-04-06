from django.db import connection


def execute_select_query(query, fetch):
    data = None
    with connection.cursor() as cursor:
        cursor.execute(query)
        if fetch == 'one':
            data = cursor.fetchone()
        else:
            data = cursor.fetchmany()

    return data


def execute_update_query(query):
    with connection.cursor() as cursor:
        cursor.execute(query)