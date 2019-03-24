import os
import unittest
from micros1client.client import Client 


class TestMclient(unittest.TestCase):
    
    
    def test_micros1_client(self):
        mcclient = Client()
        print (mcclient.get_url_to_connect(), mcclient.url_type, 
               mcclient.ssl_enabled, mcclient.ssl_verify)
        
        print(mcclient.url_to_connect)
        
        r = mcclient.ep3()
        print(r)
        
    
