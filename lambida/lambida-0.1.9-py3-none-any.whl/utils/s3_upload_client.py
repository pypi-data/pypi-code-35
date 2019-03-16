"""Upload Client for AWS Event Data to S3."""
# -*- coding: utf-8 -*-
import json
import boto3


s3 = boto3.resource('s3')


def upload_s3_file(bucket, key, data):
    """Upload Data to S3."""
    s3_object = s3.Object(bucket, key)
    response = s3_object.put(Body=data)
    return s3_object, response


def upload_raw_event(event, config):
    """Upload Raw Event."""
    s3_object, response = upload_s3_file(
        bucket=config["_BUCKET_NAME"],
        key=config["_PREFIX_TRANSIENT"] + config["_RAW_EVENT_FILENAME"],
        data=json.dumps(event))
    config["_LOG"].info('Uploaded raw event as: {}'.format(s3_object))
    return response


def upload_deadletter_event(event, config):
    """Upload Dead Letter Event."""
    s3_object, response = upload_s3_file(
        bucket=config["_BUCKET_NAME"],
        key=config["_PREFIX_TRANSIENT"] + config["_DLQ_FILENAME"],
        data=json.dumps(event))
    config["_LOG"].error('Uploaded dead letter event as: {}'.format(s3_object))
    return response



def upload_test_event(prefix_dict, config):
    """Upload Test Event."""
    upload_message_bodies(prefix_dict, config)




def upload_message_bodies(prefix_dict, config):
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


def check_equality(no_messages_uploaded, config):
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
