"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime
import DataZone

class RawData(DataZone):
    """A handler to operate on S3 with transient data."""

    def __init__(self):
        """A handler init."""
        self.prefix = "data_zones/raw_data/"
        self.raw_data_filename = "aws_lambda/" + self.function_name + "/" + \
                                 self.table_partition + \
                                 self.aws_request_id + \
                                 "_" + self.timestamp + ".json"

    def upload_deadletter_event(self, event, config):
        """Upload Dead Letter Event."""
        s3_object, response = upload_s3_file(
            bucket=config["_BUCKET_NAME"],
            key=config["_PREFIX_TRANSIENT"] + config["_DLQ_FILENAME"],
            data=json.dumps(event))
        config["_LOG"].error('Uploaded dead letter event as: {}'.format(s3_object))
        return response

    def upload_test_event(self, prefix_dict, config):
        """Upload Test Event."""
        upload_message_bodies(prefix_dict, config)


