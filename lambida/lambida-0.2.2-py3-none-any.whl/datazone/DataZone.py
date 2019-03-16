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


class DataZone(object):
    """A handler to operate on S3 data zones."""

    def __init__(self, event, context, config):
        """A handler init."""
        self.log = config["_LOG"]
        self.bucket = config["_BUCKET"]
        self.s3_client = boto3.resource('s3')

    def upload_s3_file(self, key, data):
        """Upload Data to S3."""
        s3_object = self.s3_client.Object(self.bucket, key)
        response = s3_object.put(Body=data)
        self.log.info('Uploaded Object to: {}'.format(s3_object))
        return s3_object, response

