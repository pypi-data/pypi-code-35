"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime
import lambida.datazone.utils as utils


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
        self.filename = \
            self.aws_request_id + "_" + \
            utils.get_timestamp() + ".json"
        self.s3_client = boto3.resource('s3')

    def get_prefix(self, key):
        """Return Prefix."""
        return self.location +  \
            "{}/".format(key) +  \
            "aws_lambda/" +  \
            self.function_name + "/" + \
            utils.get_table_partition_by_day() \
            

    def s3_put_request(self, key, data):
        """Upload Data to S3."""
        s3_object = \
            self.s3_client.Object(
                bucket_name=self.bucket_name, 
                key=self.get_prefix(key)+self.filename)
        response = s3_object.put(Body=data)
        if key ==self.dead_letter_key:
            self.log.error('S3 Put Requests: {}'.format(s3_object))
        else:
            self.log.info('S3 Put Requests: {}'.format(s3_object))
        
        return s3_object, response

