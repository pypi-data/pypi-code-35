"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime
import lambida.datazone.utils as utils


s3_resource = boto3.resource('s3')


class DataZone(object):
    """A handler to operate on S3 data zones."""

    def __init__(self, event, context, config):
        """A handler init."""
        self.log = config["_LOG"]
        self.bucket_name = config["_BUCKET"]
        self.dead_letter_key = "dead_letter"
        self.function_name = context.function_name
        self.aws_request_id = context.aws_request_id
        self.dead_letter_key = "dead_letter"
        self.filename = self.function_name + "_" + \
            self.aws_request_id + "_" + \
            utils.get_timestamp() + ".json"

    def get_prefix(self, key):
        """Return Prefix."""
        return self.location +  \
            "{}/".format(key) +  \
            utils.get_table_partition_by_day()

    def s3_put_request(self, key, data):
        """Upload Data to S3."""
        s3_object = \
            s3_resource.Object(
                bucket_name=self.bucket_name, 
                key=self.get_prefix(key)+self.filename)
        response = s3_object.put(Body=data)
        if key ==self.dead_letter_key:
            self.log.error('S3 Put Requests: {}'.format(s3_object))
        else:
            self.log.info('S3 Put Requests: {}'.format(s3_object))
        
        return s3_object, response

    def s3_get_object_summary(self, key):
        """Return Object Summary for a Bucket."""
        bucket = \
            s3_resource.Bucket(self.bucket_name)
        for object_summary in bucket.objects.filter(Prefix=key):
            yield object_summary



