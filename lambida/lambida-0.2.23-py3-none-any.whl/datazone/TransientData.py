"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime
from lambida.datazone.DataZone import DataZone


class TransientData(DataZone):
    """A handler to operate on S3 with transient data."""

    def __init__(self, event, context, config):
        """A handler init."""
        DataZone.__init__(self, event, context, config)
        self.location = "data_zones/transient_data/"
        self.raw_event_key = "raw_event"
        self.dead_letter_key = "dead_letter"
        self.test_key = "test_event"
        self.event = event

    def upload_raw_event(self):
        """Upload Test Event."""
        return self.s3_put_request(
            key= self.raw_event_key,
            data=json.dumps(self.event))

    def upload_dead_letter(self):
        """Upload Test Event."""
        return self.s3_put_request(
            key= self.dead_letter_key,
            data=json.dumps(self.event))

    def upload_test_event(self, data):
        """Upload Test Event."""
        return self.s3_put_request(
            key= self.test_key,
            data=json.dumps(data))
