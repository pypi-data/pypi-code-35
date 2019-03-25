import requests
import json
import jwt

# from tokenleaderclient.client.client import Client as tlClient
from linkinvclient.configs.config_handler import Configs as LIConfig

# must_have_keys_in_yml_for_ms1c = {
#                                   'url_type',
#                                   'ssl_enabled',
#                                   'ssl_verify'                            
#                                  }   

service_name = 'linkInventory'
conf_file='/etc/tokenleader/client_configs.yml'

must_have_keys_in_yml = {}   

conf = LIConfig(service_name, conf_file=conf_file, must_have_keys_in_yml= must_have_keys_in_yml)

yml = conf.yml.get(service_name)
#print(yml)


# TC = tlClient()

class LIClient():   
    '''
    First initialize an instance of tokenleader client and  pass it to MSCclient 
    as its parameter
    '''
    
    def __init__(self, tlClient ):       
        
        self.tlClient = tlClient
        self.url_type = yml.get('url_type')
        self.ssl_enabled = yml.get('ssl_verify')
        self.ssl_verify = yml.get('ssl_verify')
        self.url_to_connect = self.get_url_to_connect()
        

    def get_url_to_connect(self):
        url_to_connect = None
        catalogue = self.tlClient.get_token()['service_catalog']
        #print(catalogue)
        if catalogue.get(service_name):
            #print(catalogue.get(service_name))
            url_to_connect = catalogue[service_name][self.url_type]
        else:
            msg = ("{} is not found in the service catalogue, ask the administrator"
                   " to register it in tokenleader".format(service_name))
            print(msg)
        return url_to_connect
    
    
    def invoke_call(self, method, service_endpoint,  headers, data=None,):
        try:
            if method == 'GET':  
                r = requests.get(service_endpoint, headers=headers, verify=self.ssl_verify)
            elif method == 'POST':
                r = requests.post(service_endpoint, data, headers=headers, verify=self.ssl_verify)
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
            
        try:
            r_dict = json.loads(r.content.decode())   
        except Exception as e:
            r_dict = {"looks like server has an error processing the"
                      "the request, the response recieved is {}".format(r.text)}
                      
                    
        return r_dict
              
    
    
    def list_links(self):
        token = self.tlClient.get_token().get('auth_token')
        api_route = '/list/links'
        service_endpoint = self.url_to_connect + api_route
        headers={'X-Auth-Token': token}  
        return self.invoke_call( 'GET', service_endpoint, headers )
    
    def list_link_by_slno(self, slno):
        token = self.tlClient.get_token().get('auth_token')
        api_route = '/list/link/{}'.format(slno)
        service_endpoint = self.url_to_connect + api_route
        headers={'X-Auth-Token': token}  
        return self.invoke_call( 'GET', service_endpoint, headers )
        
    
    
    

