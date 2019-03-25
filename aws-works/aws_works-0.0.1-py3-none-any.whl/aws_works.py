'''
Aws_works
=========
It's a python module with useful actions for those who works with amazon web services through boto3(aws high-level api).

This module is a working in progress and not have a official documentation yet.

Author: Guilherme Lana
e-mail: guilherme.lana@gerdau.com.br

'''
import io
import time
import json
import boto3
import datetime
import numpy as np
import pandas as pd
from time import sleep
from dateutil.tz import tzlocal

class s3:
   
    '''Here we attribute s3 self values and actions'''
    Bucket = None
        
    def __init__(self):
        client = boto3.client('s3')
    
    def get_address(s3url):
        '''
        Input:
            path[string, list] = Expect an s3 ulr or a list of s3 urls;
        Return:
            bucket[string]
            path_file[string]
        Example:
            b, p = s3.get_address("s3://your-bucket/folder/file.format")
            
            print(b)
            "your-bucket"
            print(p)
            "folder/file.format"
        '''
        b = path.split('/')[2]
        p = path.replace('s3://{}/'.format(b),'')
        return b, p
    
    def read_csv(path_file, bucket=None):
        '''
        Input:
            path_file['string']
        '''
        obj = client.get_object(Bucket=bucket, Key=path_file)['Body']
        df = pd.read_csv(io.BytesIO(obj.read()))
        return df
    
    def write_csv(dataframe, bucket, namefile):
        obj = io.StringIO()
        dataframe.to_csv(obj, sep=',', index=False)
        client.put_object(Bucket=bucket, Key=svFolder+'/'+namefile, Body=obj.getvalue())
        return 'dataframe written on s3.'