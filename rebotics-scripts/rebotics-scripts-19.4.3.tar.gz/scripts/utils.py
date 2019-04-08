import json
from datetime import datetime

import click
import pytz
from dateutil import parser as date_parser
from prettytable import PrettyTable


def format_processing_action_output(processing_actions_list, format_):
    if format_ == 'json':
        click.echo(json.dumps(processing_actions_list, indent=2))
    elif format_ == 'id':
        click.echo(" ".join([str(item['id']) for item in processing_actions_list]))
    else:
        table = PrettyTable()
        table.field_names = ['#', 'id', 'store', 'user', 'status',
                             'created', 'last_requeue', 'last_requeue ago', 'time in queue']

        now = datetime.now(pytz.utc)
        for i, processing_action in enumerate(processing_actions_list):
            created_datetime = date_parser.parse(processing_action['created'])
            last_requeue_datetime = date_parser.parse(processing_action['last_requeue'])

            if processing_action['status'] in ['error', 'done', 'interrupted']:
                start_time = date_parser.parse(processing_action['processing_start_time'])
                finish_time = date_parser.parse(processing_action['processing_finish_time'])
                time_in_queue = finish_time - start_time
            else:
                time_in_queue = now - last_requeue_datetime
            table.add_row([
                i,
                processing_action['id'],
                '#{store_id}'.format(**processing_action),
                '{username}'.format(**processing_action['user']),
                processing_action['status'],
                created_datetime.strftime('%c'),
                last_requeue_datetime.strftime('%c'),
                str(now - last_requeue_datetime),
                str(time_in_queue),
            ])
        click.echo(table)
