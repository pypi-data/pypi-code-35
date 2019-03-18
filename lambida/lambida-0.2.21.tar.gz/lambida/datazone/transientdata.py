"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
from lambida.datazone.datazone import DataZone


class TransientData(DataZone):
    """A handler to operate on S3 with transient data."""

    def __init__(self, event, context, config):
        """A handler init."""
        DataZone.__init__(self, event, context, config)
        self.location = "data_zones/transient_data/"
        self.raw_event_key = "raw_event"
        self.dead_letter_key = "dead_letter"
        self.test_key = "test_event"
        self.error_key = "error_log"
        self.event = event

    def upload_raw_event(self):
        """Upload Test Event."""
        return self.s3_put_request(
            key=self.raw_event_key,
            data=json.dumps(self.event))

    def upload_dead_letter(self):
        """Upload Test Event."""
        return self.s3_put_request(
            key=self.dead_letter_key,
            data=json.dumps(self.event))

    def upload_error_event(self):
        """Upload Error Event."""
        return self.s3_put_request(
            key=self.error_key+self.event['logGroup'],
            data=json.dumps(self.event))

    def upload_test_event(self, data):
        """Upload Test Event."""
        return self.s3_put_request(
            key=self.test_key,
            data=json.dumps(data))

    def s3_folder_empty(self, key):
        """Checks if a Folder in S3 is empty."""
        for object_summary in self.s3_get_object_summary(key):
            return object_summary


