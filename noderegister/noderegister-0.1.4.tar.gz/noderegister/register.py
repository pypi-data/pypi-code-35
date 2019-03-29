#!/usr/bin/env python
from __future__ import print_function
from ec2_metadata import ec2_metadata

import argparse
import sys
import os
import boto3
import uuid
from tabulate import tabulate


#print (ec2_metadata.private_hostname)
#print (ec2_metadata.private_ipv4)

class NodeRegister(object):

    def __init__(self, ddb_table):
        ddb_resource = boto3.resource('dynamodb', region_name='us-west-2')
        try:
            self.ddb_table = ddb_resource.Table(ddb_table)
        except Exception as _error:
            print(_error)

    def register(self, hostname, private_ip):
        print('Registering Node => {}'.format(hostname))
        self.ddb_table.put_item(
            Item={
                'hostname': hostname,
                'private-ip': private_ip,
                'node-type': 'unassigned'
            }
        )
def db_init(table_name):

    ddb_resource = boto3.resource('dynamodb', region_name='us-west-2')
    try:
        table = ddb_resource.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'hostname',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'hostname',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )
        print('Creating ...... Table ->[{}]'.format(table_name))
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
        return table
    except Exception as table_exists:
        if table_exists:
            print('Using Existing Table...... ->[{}]'.format(table_name))
            table = ddb_resource.Table(table_name)
            table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
            return table

def node_count(query_type=None):
    ddb_resource = boto3.resource('dynamodb', region_name='us-west-2')
    try:
        table = ddb_resource.Table(table_name)
        response = table.get_item(
            Item={
                'hostname': hostname,
                'node-type': role
                }
        )
        return response
    except Exception as _error:
        print(_error)

def db_list(table_name):
    ddb_resource = boto3.resource('dynamodb', region_name='us-west-2')
    try:
        table = ddb_resource.Table(table_name)

        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

        print(tabulate(data))
    except Exception as _error:
        print(_error)

def is_ec2():
    try:
        if ec2_metadata.instance_id:
            return True
    except Exception:
       return False

def assign_role(table_name, hostname, private_ip, role):
    ddb_resource = boto3.resource('dynamodb', region_name='us-west-2')
    try:
        table = ddb_resource.Table(table_name)
        response = table.put_item(
            Item={
                'hostname': hostname,
                'private-ip': private_ip,
                'node-type': role
                }
        )
        return response
    except Exception as _error:
        print(_error)


parser = argparse.ArgumentParser()
parser.add_argument("-c", "--create_ddb", help="Create a new DynamoDB table", action='store_true')
action_createdb = parser.add_argument_group('actions')
action_group = action_createdb.add_mutually_exclusive_group()
action_group.add_argument("-a", "--assign", help="Set the node type of an existing node")
action_group.add_argument("-r", "--register_node", help="Add a new node to the DynamoDB table", action='store_true')
action_group.add_argument("-l", "--list", help="List Registered Node in given DynamoDB Table", action='store_true')
required_group = parser.add_argument_group('required', 'for (assign|list|register_node) actions')
required_group.add_argument("-D", "--dynamodb_table", help="Name of Existing DynamoDB")
args = parser.parse_args()

def is_register(ddb_table):
    dynamodb = boto3.client('dynamodb', region_name='us-west-2')
    existing_tables = dynamodb.list_tables()
    if ddb_table in existing_tables['TableNames']:
        #print(existing_tables['TableNames'])
        return True
    else:
        print('Table {} does not exist in the specified region'.format(ddb_table))
        return False
        sys.exit(1)

def main():
    ddb = None

    if args.create_ddb:
        if len(sys.argv) <= 2:
            ddb='noderegister-{}'.format(str(uuid.uuid4()))
            db_init(ddb)
            print ('Pass the -D flag to use this DynamoDBTable \n\t EXAMPLE: {} -D {}'.format(os.path.basename(__file__), ddb))
            sys.exit(0)
        else:
            print ('Too many args --create_ddb does not require a value \n\t EXAMPLE: {} -c'.format(os.path.basename(__file__)))
            sys.exit(1)

    elif args.list:
        if args.dynamodb_table:
            if is_register(args.dynamodb_table):
                db_list(args.dynamodb_table)
                sys.exit(0)
        else:
            print('Node register not found! --list operation requires you to pass in an existing DynamoDB')
            print('EXAMPLE: \n\t{} -D Existing-DynamoDb-Name -l'.format(os.path.basename(__file__), ddb))

    elif args.assign:
        if args.dynamodb_table:
            if is_register(args.dynamodb_table):
                assign_role(args.dynamodb_table, ec2_metadata.private_hostname, ec2_metadata.private_ipv4, args.assign)
        else:
            print('Node register not found! --assign operation requires you to pass in an existing DynamoDB')
            print('EXAMPLE: \n\t{} -D Existing-DynamoDb-Name -a master'.format(
            os.path.basename(__file__), ddb))

    elif args.register_node:
        if args.dynamodb_table:
            if is_register(args.dynamodb_table):
                #Create Node Register Table
                if not is_ec2():
                    print('This utility is only supported on AWS ec2')
                else:
                    new_register = NodeRegister(args.dynamodb_table)
                    new_register.register(ec2_metadata.private_hostname,ec2_metadata.private_ipv4)
        else:
            print('Node register not found! --regiser_node operation requires you to pass in an existing DynamoDB')
            print('EXAMPLE: \n\t{} -D Existing-DynamoDb-Name -r'.format(
            os.path.basename(__file__), ddb))
    else:
        parser.print_help()
