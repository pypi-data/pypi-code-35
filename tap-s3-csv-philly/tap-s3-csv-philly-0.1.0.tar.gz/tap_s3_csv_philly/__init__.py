#!/usr/bin/env python3
import os
import json
import singer   
import csv
import boto3
import botocore
from singer import utils, metadata

REQUIRED_CONFIG_KEYS = ["bucket_name", "file_name", "aws_access_key_id", "aws_secret_access_key"]
LOGGER = singer.get_logger()


def download_file_s3(bucket_name, file, aws_access_key_id, aws_secret_access_key):
    try:
        LOGGER.info("Downloading the file")
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id , aws_secret_access_key=aws_secret_access_key)
        s3.download_file(bucket_name,file,'new_file.csv')

    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            LOGGER.info("The object does not exist.")
        else:
            raise

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

# Load schemas from schemas folder
def load_schemas():
    schemas = {}

    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = json.load(file)

    return schemas
def load_metadata(schema,key_properties=None,replication_keys=None):
    return [
            {
                "metadata":{
                    'replication-method':'INCREMENTAL',
                    'selected': True,
                    'schema-name':schema,
                    'valid-replication-keys': replication_keys,
                    'table-key-properties': key_properties,
                    "inclusion": "available",
                },
                "breadcrumb": []
            }
        ]
def discover():
    raw_schemas = load_schemas()
    streams = []

    for schema_name, schema in raw_schemas.items():

        # TODO: populate any metadata and stream's key properties here..
        stream_metadata = []
        stream_key_properties = []

        if schema_name=="wireless_products":
            LOGGER.info("Discovering wireless_products")
            replication_keys=['NPA']
            key_properties=['NXX']
            stream_metadata=load_metadata(schema_name,key_properties,replication_keys)

        # create and add catalog entry
        catalog_entry = {
            'stream': schema_name,
            'tap_stream_id': schema_name,
            'schema': schema,
            'metadata' : stream_metadata,
            'key_properties': key_properties
        }
        streams.append(catalog_entry)

    return {'streams': streams}

def get_selected_streams(catalog):
    '''
    Gets selected streams.  Checks schema's 'selected' first (legacy)
    and then checks metadata (current), looking for an empty breadcrumb
    and mdata with a 'selected' entry
    '''

    selected_streams = []
    for stream in catalog['streams']:
        stream_metadata = metadata.to_map(stream['metadata'])

        if metadata.get(stream_metadata, (), "selected"):
            selected_streams.append(stream['tap_stream_id'])

    return selected_streams

def update_state(STATE,schema_name,record):
    if schema_name=="wireless_products":
        replication_key='NPA'
        utils.update_state(STATE,schema_name, record[replication_key])

def handle_sync(stream_id, stream_schema,filename,STATE):
    if stream_id=="wireless_products":
        f= open("new_file.csv","r")
        reader = csv.reader(f, delimiter=',', quotechar='"') 
        next(reader, None)
        for line in reader:
            flattened={}
            try:
                lastdata=line[4]
            except:
                lastdata=""
            keys=[key for key in stream_schema['properties'].keys()]  

            flattened[keys[0]]= None if line[0] is None else int(line[0])
            flattened[keys[1]]= None if line[1] is None else int(line[1])
            flattened[keys[2]]= None if line[2] is None else int(line[2])
            flattened[keys[3]]= "" if line[3] is None else line[3]
            flattened[keys[4]]= lastdata

            singer.write_record(stream_id, flattened)
            state=update_state(STATE,stream_id,flattened)
            singer.write_state(state)

def sync(config, state, catalog):

    selected_stream_ids = get_selected_streams(catalog)
    LOGGER.info(selected_stream_ids)
    # Loop over streams in catalog
    for stream in catalog['streams']:
        STATE={}
        stream_id = stream['tap_stream_id']
        stream_schema = stream['schema']
        if stream_id in selected_stream_ids:
            # TODO: sync code for stream goes here...
            singer.write_schema(stream_id, stream_schema, stream['key_properties'])
            download_file_s3(config['bucket_name'],config['file_name'],config['aws_access_key_id'],config['aws_secret_access_key'])
            LOGGER.info("Running..")
            handle_sync(stream_id,stream_schema,"new_file.txt", STATE)
            LOGGER.info('Syncing stream:' + stream_id)
    return

@utils.handle_top_exception(LOGGER)
def main():

    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        print(json.dumps(catalog, indent=2))
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog =  discover()

        sync(args.config, args.state, catalog)

if __name__ == "__main__":
    main()
