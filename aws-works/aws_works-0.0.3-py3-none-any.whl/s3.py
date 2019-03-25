'''
Aws_works.s3
============
It's a python module with useful actions for those who works with amazon web services through boto3(aws high-level api).

Here we focus in s3 bucket like an object. It means you set a bucket and execute some actions in it.
============
'''

import io
import json
import boto3
import numpy as np
import pandas as pd


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
    if(s3url.startswith('s3://')):
        b = []
        p = []
        if(type(s3url)==str):
            s3url = [s3url]
        for url in s3url:
            tmp = url.split('/')[2]
            tmp2 = url.replace('s3://{}/'.format(tmp),'')
            b.append(tmp)
            p.append(tmp2)
        if((len(b)==1)&(len(p)==1)):
            return b[0], p[0]
        else:
            return b, p
    else:
        print('not a s3 url')

class s3_bucket:
   
    '''Here we attribute s3 a bucket to work'''
    Bucket = None
    
    def __init__(self, name):
        self.Bucket = name #public
        self.__alias = client #private
    
    def read_csv(self, path):
        '''
        Read from s3 a csv file
        -----------------------
        Input:
            path[string] = Expect the path to the csv file to be readed.
        -----------------------
        return:
            dataframe[pandas.dataframe]
        -----------------------
        Example:
            df = s3_bucket.read_csv(path='folder/file.csv')
        -----------------------
        '''
        try:
            obj = client.get_object(Bucket=self.Bucket, Key=path)['Body']
            df = pd.read_csv(io.BytesIO(obj.read()))
            return df
        except:
            raise
    
    def read_log(self, path, output_format='pandas'):
        '''
        Read from s3 a log file in json.
        -------------------------------
        Input:
            path[string] = Expect the path to the json file to be readed.
            output_format['pandas'|'json'] = Specify the format you desire as output, pandas is default.
        -------------------------------
        Return:
            Depending on output_format specified will return or a pandas.dataframe or a json.
        -------------------------------
        Example:
            logDF = s3_bucket.read_log(path='folder/file.json')
        -------------------------------
        '''
        obj = client.get_object(Bucket=self.Bucket,Key=path)['Body']
        jobj = json.loads(obj.read())
        if(output_format=='pandas'):
            logDf = pd.DataFrame(data=jobj['data'],columns=jobj['columns'],index=list(np.arange(0,len(jobj['data']))))
            return logDf
        if(output_format=='json'):
            return jobj
        else:
            print('output_format not specified correctly.')
    
    def write_csv(self, dataframe, path_name):
        '''
        Write a pandas dataframe into s3.
        ---------------------------------
        Input:
            dataframe[pandas.dataframe] = Expect a pandas dataframe to be written into s3.
            path_name[string] = Specify the path and name you desire to save your file.
        ---------------------------------
        Return:
            String - dataframe written into s3 bucket.
        ---------------------------------
        Example:
            s3_bucket.write_csv(dataframe, namefile='folder/my_dataframe')
        ---------------------------------
        '''
        namefile = namefile.replace('.csv','')
        obj = io.StringIO()
        dataframe.to_csv(obj, sep=',', index=False)
        client.put_object(Bucket=self.Bucket, Key=path_name+'.csv', Body=obj.getvalue())
        return 'dataframe written into s3.'
    
    def write_log(self, dictionary, path):
        '''
        This method writes logs into s3.
        --------------------------------
        Input:
            dictionary[dict] = Expect a dictionary structured as json files.
            Log description:
                To create a log file we highly recomed to create a json structure, such as:
                {
                    'columns' : [],
                    'data' : []
                }
            path[string] = Expect a string with the path to write the json.
        --------------------------------
        Return:
            String - 'log updated/created'
        --------------------------------
        Example:
        tmp = {
            'columns':['A','B'],
            'data':[[0.001, 0.002],[0.003, 0.004]]
        }
            s3_bucket.write_log(dictionary=tmp, path='sql_exec/logs/log.json')
            
        return:
            log updated
        --------------------------------
        '''
        try:
            obj = client.get_object(Bucket=self.Bucket, Key=path)['Body']
            jobj = json.loads(obj.read())
            jobj['data'] = jobj['data']+dictionary['data']
            client.put_object(Bucket=self.Bucket, Key=path, Body=json.dumps(jobj))
            return 'log updated'
        except:
            client.put_object(Bucket=self.Bucket, Key=path, Body=json.dumps(dictionary))
            return 'log created'