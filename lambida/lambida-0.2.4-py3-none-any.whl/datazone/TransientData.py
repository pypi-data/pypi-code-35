"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime
from lambida.datazone.DataZone import DataZone
import lambida.datazone.utils as utils


class TransientData(DataZone):
    """A handler to operate on S3 with transient data."""

    def __init__(self, event, context, config):
        """A handler init."""
        self.event = event
        DataZone.__init__(self, self.event, context, config)
        self.function_name = context.function_name
        self.prefix = "data_zones/transient_data/"
        self.aws_request_id = context.aws_request_id
        self.raw_event_filename = \
            "aws_lambda/" + self.function_name + "/" + \
            "raw_event_data/" + utils.get_table_partition_by_day() + \
            "raw_event_" + self.aws_request_id + \
            "_" + utilsget_timestamp() + ".json"
        self.dlq_filename = \
            "aws_lambda/" + self.function_name + "/" + \
            "dead_letters/" + utils.get_table_partition_by_day() + \
            "dlq_event_" + self.aws_request_id + \
            "_" + utils.get_timestamp() + ".json"

    def upload_raw_event(self):
        """Upload Raw Event."""
        return self.upload_s3_file(
            key=self.prefix + self.raw_event_filename,
            data=json.dumps(self.event))

    def upload_dead_letter(self):
        """Upload Raw Event."""
        return self.upload_s3_file(
            key=self.prefix + self.dlq_filename,
            data=json.dumps(self.event))

