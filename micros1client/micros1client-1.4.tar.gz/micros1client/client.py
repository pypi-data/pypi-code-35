import os
import requests
import json
import jwt

# from tokenleaderclient.client.client import Client as tlClient
from micros1client.configs.config_handler import Configs as MSConfig

# must_have_keys_in_yml_for_ms1c = {
#                                   'url_type',
#                                   'ssl_enabled',
#                                   'ssl_verify'                            
#                                  }   

service_name = 'micros1'
conf_file='/etc/tokenleader/client_configs.yml'

must_have_keys_in_yml = {}   

conf = MSConfig(service_name, conf_file=conf_file, must_have_keys_in_yml= must_have_keys_in_yml)

micros1_yml = conf.yml.get(service_name)


class MSClient():   
    '''
    First initialize an instance of tokenleader client and  pass it to MSCclient 
    as its parameter
    '''
    
    def __init__(self, tlClient ):       
        
        self.tlClient = tlClient
        self.url_type = micros1_yml.get('url_type')
        self.ssl_enabled = micros1_yml.get('ssl_verify')
        self.ssl_verify = micros1_yml.get('ssl_verify')
        self.url_to_connect = self.get_url_to_connect()
        

    def get_url_to_connect(self):
        url_to_connect = None
        try:
            catalogue = self.tlClient.get_token()['service_catalog']
        #print(catalogue)
            if catalogue.get(service_name):
                #print(catalogue.get(service_name))
                url_to_connect = catalogue[service_name][self.url_type]
            else:
                msg = ("{} is not found in the service catalogue, ask the administrator"
                       " to register it in tokenleader".format(service_name))
                print(msg)
        except:
            print("could not retrieve service_catalog from token leader," 
                  " is token leaader service running ?"
                  " is tokenleader reachable from this server/container ??")
        return url_to_connect
    
    
    def get_service_ep_n_auth_header(self, api_route, service_name=service_name):
        ''' url to connect method was not caturing the exception when service enfpoint
        construction fails for non availability of tokenleader. Also there  call to 
        tokenleader used to be  twice. This code will correct the above issues but need to 
        be tested'''       
        url_to_connect = None
        try:
            all_data_token = self.tlClient.get_token()
            auth_token = all_data_token.get('auth_token')
            headers_v={'X-Auth-Token': auth_token}
            catalogue = all_data_token.get('service_catalog')            
            api_route = api_route            
        #print(catalogue)
            if catalogue.get(service_name):
                #print(catalogue.get(service_name))
                url_to_connect = catalogue[service_name][self.url_type]
                service_endpoint_v = url_to_connect + api_route
            else:
                msg = ("{} is not found in the service catalogue, ask the administrator"
                       " to register it in tokenleader".format(service_name))
                print(msg)
        except:
            print("could not retrieve service_catalog from token leader," 
                  " is token leaader service running ?"
                  " is tokenleader reachable from this server/container ??")
        return service_endpoint_v,  headers_v
    
    
    def ep3(self):        
        api_route = '/ep3'
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)         
        try:  
            r = requests.get(service_ep, headers=headers, verify=self.ssl_verify)
            r_dict = json.loads(r.content.decode())   
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
        return r_dict
    
    
    def upload_xl(self, filepath):
        token = self.tlClient.get_token().get('auth_token')
        api_route = '/invoice/uploadxl'
        service_endpoint = self.url_to_connect + api_route
        headers={'X-Auth-Token': token}
        files = {'file': ( os.path.basename(filepath), 
                          open(filepath, 'rb'), 
                          'application/vnd.ms-excel', 
                          {'Expires': '0'})}
        try:  
            r = requests.post(service_endpoint, headers=headers, 
                             files=files, verify=self.ssl_verify)              
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
        try:
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {"Content returned by the server is not json serializable"
                      " checking the server log  might  help. "
                      " the text returned by the server is {}".format(r.text)}                      
        return r_dict
    
    
    def list_invoices(self, field_name, field_value, level):
        token = self.tlClient.get_token().get('auth_token')
        api_route = '/invoice/list/{}/{}/{}'.format(
            field_name, field_value, level)
        service_endpoint = self.url_to_connect + api_route
        headers={'X-Auth-Token': token}
        try:  
            r = requests.get(service_endpoint, headers=headers, 
                            verify=self.ssl_verify)              
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
        try:
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {"Content returned by the server is not json serializable"
                      " checking the server log  might  help. "
                      " the text returned by the server is {}".format(r.text)}
        return r_dict
    
    
    def list_invoices_clo(self, field_name, field_value):
        token = self.tlClient.get_token().get('auth_token')
        api_route = '/invoice/listclo/{}/{}'.format(
            field_name, field_value)
        service_endpoint = self.url_to_connect + api_route
        headers={'X-Auth-Token': token}
        try:  
            r = requests.get(service_endpoint, headers=headers, 
                            verify=self.ssl_verify)              
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}
        try:
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {"Content returned by the server is not json serializable"
                      " checking the server log  might  help. "
                      " the text returned by the server is {}".format(r.text)}
        return r_dict
    

    def update_invoice(self, filepath):
            token = self.tlClient.get_token().get('auth_token')
            api_route = '/invoice/update'
            service_endpoint = self.url_to_connect + api_route
            headers={'X-Auth-Token': token}
            files = {'file': ( os.path.basename(filepath), 
                              open(filepath, 'rb'), 
                              'application/vnd.ms-excel', 
                              {'Expires': '0'})}
            try:  
                r = requests.put(service_endpoint, headers=headers, 
                                 files=files, verify=self.ssl_verify)              
            except Exception as e:
                r_dict = {'error': 'could not conect to server , the error is {}'.format(e)} 
            try:
                r_dict = json.loads(r.content.decode())
            except Exception as e:
                r_dict = {"Content returned by the server is not json serializable"
                          " checking the server log  might  help. "
                          " the text returned by the server is {}".format(r.text)}
            return r_dict

              
    def delete_invoices(self, inv_num):
        token = self.tlClient.get_token().get('auth_token')
        api_route = '/invoice/delete/{}'.format(inv_num)
        service_endpoint = self.url_to_connect + api_route
        headers={'X-Auth-Token': token}
        try:  
            r = requests.delete(service_endpoint, headers=headers, 
                            verify=self.ssl_verify)              
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}    #     
        
#         print(r)  # for displaying from the cli  print in cli parser
        try:
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {"Content returned by the server is not json serializable"
                      " checking the server log  might  help. "
                      " the text returned by the server is {}".format(r.text)}
        return r_dict
    
    
    def recommend_changes(self, listdata):
        api_route = '/invoice/recommend'
        service_ep, headers = self.get_service_ep_n_auth_header(api_route)
        headers.update({'content-type':'application/json'})
        try:  
            r = requests.put(service_ep, 
                             headers=headers, 
                             data = json.dumps(listdata),                             
                            verify=self.ssl_verify)              
        except Exception as e:
            r_dict = {'error': 'could not conect to server , the error is {}'.format(e)}    #     
            print(r_dict)
#         print(r)  # for displaying from the cli  print in cli parser
        
        try:
            r_dict = json.loads(r.content.decode())
        except Exception as e:
            r_dict = {"Content returned by the server is not json serializable"
                    " checking the server log  might  help. "
                    " the text returned by the server is {}".format(r.text)}
        return r_dict
