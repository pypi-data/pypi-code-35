import requests

from . import _response_handler

def get (url,
         header_parameters=None,
         query_parameters=None):

    response = requests.get(url=url,
                            params=query_parameters, 
                            headers=header_parameters)

    return _response_handler.handle(response)

def post (url, 
          header_parameters=None,
          query_parameters=None, 
          body_parameters=None): 

    response = requests.post(url=url,
                             params=query_parameters, 
                             headers=header_parameters, 
                             data=body_parameters)

    return _response_handler.handle(response)

def put (url,
         header_parameters=None,
         query_parameters=None,
         body_parameters=None):

    pass