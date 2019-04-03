"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime


def get_table_partition_by_day():
    """Return Partition Style String."""
    year = str(datetime.date.today().year)
    month = str(datetime.date.today().month)
    day = str(datetime.date.today().day)
    return "year=" + year + \
           "/month=" + month + \
           "/day=" + day + "/"


def get_timestamp():
    return datetime.datetime.now().replace(microsecond=0).isoformat()


