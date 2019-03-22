#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
 File: response_parser.py
 File Created: Sunday, 24th February 2019 8:09:51 pm
 Author: ESR - Romeren (emilromer@hotmail.com)
 -----
 Copyright 2019 OpenSourced, OpenSourced
 -----
 Last Modified:
 Date	By	Comments
 -----
"""
import json
import asyncio
import pandas as pd


class response_parser(object):
    """
        Class definition of a how to parse a influx response
    """
    def parse(self, response):
        if(asyncio.isfuture(response)):
            return self.parse_response_async(response)
        return self.parse_response(response)

    def parse_response(self, response):
        """
            Parse a response
        """
        raise NotImplementedError('This is a abstract definition, please implement your own')

    async def parse_response_async(self, response):
        """
            Async wrapper for parse response
        """
        response = await response
        return self.parse_response(response)

class string_parse(response_parser):
    """
        Class definition for parsing to string
    """

    def parse_response(self, response):
        """
            Parse response to a string
        """
        return response.body.decode("utf-8")

class json_parse(response_parser):
    """
        Class definition for parsing to string
    """

    def parse_response(self, response):
        """
            Parse response to a string
        """
        return json.loads(response.body.decode("utf-8"))

class dataframe_parser(response_parser):
    """
        Class definition for parsing to a pandas dataframe
    """

    def parse_response(self, response):
        """
            Parse response into a pandas dataframe
        """
        response_converted = self.response_to_dataframe(response)
        return response_converted

    def response_to_dataframe(self, response):
        """
            Takes a 200 OK response object and parses the data into a dataframe
        """
        response_converted = [json.loads(x) for x in response.body.decode("utf-8").split('\n') if x]
        
        result = None
        for body in response_converted:
            for r in body.get('results', []):
                for s in r.get('series', []):
                    df = pd.DataFrame(s['values'], columns=s['columns'])
                    if('time' in df.columns):
                        df.time = pd.to_datetime(df.time)
                        df = df.set_index('time')
                    
                    if(result is None):
                        result = df
                    else:
                        result = pd.concat([result, df])

        # Concat all results:
        if(result is None):
            return self.get_empty_dataframe()

        return result

    def get_empty_dataframe(self):
        """
            returns a empty dataframe
        """
        return pd.DataFrame()
