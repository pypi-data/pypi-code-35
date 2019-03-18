"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3
import datetime


class DataZone:
    """A handler to operate on S3 data zones."""

    def __init__(self, event, context, config):
        """A handler init."""
        self.event = event
        self.function_name = context.function_name
        self.aws_request_id = context.aws_request_id
        self.log = config["_LOG"]
        self.timestamp = \
            datetime.datetime.now().replace(microsecond=0).isoformat()
        self.year = str(datetime.date.today().year)
        self.month = str(datetime.date.today().month)
        self.day = str(datetime.date.today().day)
        self.table_partition = "year=" + self.year + \
                               "/month=" + self.month + \
                               "/day=" + self.day + "/"
        self.bucket = config["_BUCKET"]
        self.raw_event_filename = "aws_lambda/" + self.function_name + "/" + \
                                  "raw_event_data/" + self.table_partition + \
                                  "raw_event_" + self.aws_request_id + \
                                  "_" + self.timestamp + ".json"
        self.dlq_filename = "aws_lambda/" + self.function_name + "/" + \
                            "dead_letters/" + self.table_partition + \
                            "dlq_event_" + self.aws_request_id + \
                            "_" + self.timestamp + ".json"
        self.s3_client = boto3.resource('s3')

    def upload_s3_file(self, bucket, key, data):
        """Upload Data to S3."""
        s3_object = self.s3.Object(bucket, key)
        response = s3_object.put(Body=data)
        return s3_object, response


class TransientData(DataZone):
    """A handler to operate on S3 with transient data."""

    pass
    '''
    def __init__(self):
        """A handler init."""
        self.prefix = "data_zones/transient_data/"
        self.raw_event_filename = "aws_lambda/" + self.function_name + "/" + \
                                  "raw_event_data/" + self.table_partition + \
                                  "raw_event_" + self.aws_request_id + \
                                  "_" + self.timestamp + ".json"
        self.dlq_filename = "aws_lambda/" + self.function_name + "/" + \
                            "dead_letters/" + self.table_partition + \
                            "dlq_event_" + self.aws_request_id + \
                            "_" + self.timestamp + ".json"
    '''

class RawData(DataZone):
    """A handler to operate on S3 with transient data."""

    def __init__(self):
        """A handler init."""
        self.prefix = "data_zones/raw_data/"
        self.raw_data_filename = "aws_lambda/" + self.function_name + "/" + \
                                 self.table_partition + \
                                 self.aws_request_id + \
                                 "_" + self.timestamp + ".json"

    def upload_raw_event(self):
        """Upload Raw Event."""
        s3_object, response = self.upload_s3_file(
            bucket=self.bucket,
            key=self.prefix_transient + self.raw_data_filename,
            data=json.dumps(self.event))
        self.log.info('Uploaded Raw Event as: {}'.format(s3_object))
        return response

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

    def upload_message_bodies(self, prefix_dict, config):
        """Upload Messages to S3 Sorted by Prefix."""
        no_messages_uploaded = 0
        for key, value in prefix_dict.items():
            obj = str()
            for i in value:
                data = json.dumps(i)
                obj = str(obj) + str(data) + '\n'
                no_messages_uploaded += 1
            s3_object, response = upload_s3_file(
                bucket=config["_BUCKET_NAME"],
                key=config["_PREFIX_RAW_DATA"] + key + '/' + config["_RAW_DATA_FILENAME"],
                data=json.dumps(obj))
            if key == config["_DEAD_LETTER_PREFIX"]:
                config["_LOG"].error('Uploaded File as S3 DLQ: {}'.format(s3_object))
            else:
                config["_LOG"].info('Uploaded as: {}'.format(s3_object))
        check_equality(no_messages_uploaded, config)
        return response

    def check_equality(self, no_messages_uploaded, config):
        """Check equality of received and uploaded messages."""
        try:
            assert no_messages_uploaded == config["_MSG_RECEIVED"]
            config["_LOG"].info('Uploaded {} messages to S3 and {} received.'
                                .format(no_messages_uploaded,
                                        config["_MSG_RECEIVED"]))
        except:
            config["_LOG"].error('Uploaded {} messages to S3, but {} received.'
                                 .format(no_messages_uploaded,
                                         config["_MSG_RECEIVED"]))
            return True
