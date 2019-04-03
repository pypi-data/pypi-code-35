"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
from lambida.datazone.DataZone import DataZone

class RawData(DataZone):
    """A handler to operate on S3 with transient data."""

    def __init__(self, event, context, config):
        """A handler init."""
        DataZone.__init__(self, event, context, config)
        self.location = "data_zones/raw_data/"

    def upload_raw_data(self, key, data):
        """Upload Test Event."""
        return self.s3_put_request(
            key= key,
            data=json.dumps(data))



