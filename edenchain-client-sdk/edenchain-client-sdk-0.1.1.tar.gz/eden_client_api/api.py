"""
Eden SDK for client python interface
"""
import urllib
import requests
import os
import base64
import uuid
import json
import asyncio
import eth_keys
import binascii
from Crypto.Hash import keccak

from .config import EdenConfig

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Utility functions

# Request for Gets
def requestsGet(url='', data='' ):
    headers = {'content-type': 'application/json'}
    return requests.get(url=url, data=data , headers=headers, verify= False)


# Request for Post
def requestsPost(url='', data ='' ):
    headers = {'content-type': 'application/json'}
    return requests.post(url=url, data = data, headers=headers, verify = False)


# Json RPC Request Methods
API_SIGN_IN_USER  = 'user.signin'
API_GET_USER_INFO='user.get_info'
API_GET_USER_BALANCE ='user.getbalance'
API_GET_USER_TRANSACTION='user.lstransaction'
API_GET_COIN_SERVER_ADDRESS='server.coinhdaddress'
API_ADD_ETH_ADDRESS='eth.add_address'
API_DEL_ETH_ADDRESS='eth.del_address'
API_DEPOSIT_TOKEN='user.deposit'
API_WITHDRAW_TOKEN='user.withdraw'


""" 
API user sdk default class
"""

class EdenClientApi:
    
    # Network Constant
    EDENCHAIN_MAINNET_NETWORK = 0
    EDENCHAIN_BETA_RELEASE = 1
    EDENCHAIN_CANDIDATE_RELEASE = 2

    def __init__(self, network):
        (result, config) = EdenConfig().getConfig(network)
        if result == False:
            raise Exception('Network is invalid')        
        else:
            self.config = config        

    """
        create default JsonRpc Requests Objects.
    """
    def makeJsonRpcRequest(self, method, token):
        id = str(uuid.uuid4())
        params = {}
        params["iamtoken"] = token
        payload = { "method": method, "params": params , "jsonrpc": "2.0", "id": id , }
        return payload

    """
        Authenticate
    """
    def authenticate_user(self, email, password):
        payload = {'email': email , 'password': password , 'returnSecureToken':'true'}
        auth_url = 'https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key='+self.config['api_key']
        user_auth = requests.post( auth_url, data=json.dumps(payload)).json()
        token=user_auth['idToken']

        if token is None or token == '':
            return None

        if self.sign_in_user(token):
            return token

        return None

    """
        Sign In
    """
    async def sign_in_user_async(self, token):
        res = await asyncio.get_event_loop().run_in_executor(None, self.sign_in_user,  token)
        return res


    def sign_in_user(self, token=''):

        payload = self.makeJsonRpcRequest(API_SIGN_IN_USER, token)
        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return None
        
        data  = res.json()
 
        if data['id'] != payload['id']:
            return None
        
        if data["result"]["err_code"] == 0:
            return True
        else:
            return False

    """
        Get user info from IAM
    """
    async def get_user_info_async(self, token):
        res = await asyncio.get_event_loop().run_in_executor(None, self.get_user_info,  token)
        return res


    def get_user_info(self, token=''):

        payload = self.makeJsonRpcRequest(API_GET_USER_INFO, token)
        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return None
        
        data  = res.json()
 
        if data['id'] != payload['id']:
            return None
        else:
            if data['result'] is None:
                return None
            else:
                return data["result"]["data"]


    """
        Token which I have is valid or not?
    """
    async def is_token_valid_async(self, token):
        res = await asyncio.get_event_loop().run_in_executor(None, self.is_token_valid,  token)
        return res

    def is_token_valid(self, token):
        res = self.get_user_info(token)
        if res is not None and res.get('tedn_public_key'):
            return True
        else:            
            return False



    """
        Get User Balance
    """
    async def get_balance_async(self, token=''):
         res = await asyncio.get_event_loop().run_in_executor(None, self.get_user_balance,  token) 
         return res

    def get_user_balance(self, token=''):

        payload = self.makeJsonRpcRequest(API_GET_USER_BALANCE, token)
        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return None        

        data = res.json()

        if data['id'] != payload['id']:
            return None

        return data["result"]["data"]["amount"]


    """
        Get User Transaction
    """
    async def get_user_transaction_async(self, token='',page=0,countperpage=0):
         res = await asyncio.get_event_loop().run_in_executor(None, self.get_user_transaction,  token, page, countperpage) 
         return res

    def get_user_transaction(self,token='', page = 0, countperpage = 0):

        payload = self.makeJsonRpcRequest(API_GET_USER_TRANSACTION, token)
        payload["params"]["page"] = page
        payload["params"]["countperpage"] = countperpage
        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return None        
        
        data = res.json()

        if data['id'] != payload['id']:
            return None

        return data["result"]["data"]
        
    """
        Get Coin Server Address
    """
    async def  get_coin_server_address_async(self, token=''):
         res = await asyncio.get_event_loop().run_in_executor(None, self. get_coin_server_address,  token) 
         return res

    def get_coin_server_address(self, token=''):

        payload = self.makeJsonRpcRequest(API_GET_COIN_SERVER_ADDRESS, token)
        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return None        
        
        data = res.json()

        if data['id'] != payload['id']:
            return None

        return data["result"]["data"]["hdaddress"]





    def remove0xHeader(self, hexString):
        if hexString[:2] == '0x':
            return hexString[2:]
        else:
            return hexString

    def formSignature(self, hexString):
        if hexString[-2:] == '01':
            hexString = hexString[:-2]+'1c'
        else:
            hexString = hexString[:-2]+'1b'
        return hexString


    """
        Add Eth Address to iam
    """
    async def  add_eth_address_async(self, token='', private_key=''):
         res = await asyncio.get_event_loop().run_in_executor(None, self. add_eth_address,  token, private_key) 
         return res

    def add_eth_address(self, token='', private_key=''):

        # Create Address Object.
        private_key = self.remove0xHeader(private_key)

        privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(private_key))
        address  = privKey.public_key.to_checksum_address()
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(address.encode())
        hash_msg = keccak_hash.digest()
        signature = privKey.sign_msg_hash(hash_msg)

        payload = self.makeJsonRpcRequest(API_ADD_ETH_ADDRESS, token)
        payload["params"]["address"]  = address
        payload["params"]["public_key"]  = self.remove0xHeader(privKey.public_key.to_hex())
        payload["params"]["signature"] = self.formSignature(signature.to_hex())
       
        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return False
        
        data = res.json()

        if data['id'] != payload['id']:
            return False
       
        if data["result"]["err_code"] == 0:
            return True
        else:
            return False
        
    """
        Del Eth Address to iam
    """
    async def  del_eth_address_async(self, token='', private_key=''):
        res = await asyncio.get_event_loop().run_in_executor(None, self. del_eth_address,  token, private_key ) 
        return res

    def del_eth_address(self, token='', private_key=''):

        # Create Address Object.
        private_key = self.remove0xHeader(private_key)

        privKey = eth_keys.keys.PrivateKey(binascii.unhexlify(private_key))
        address  = privKey.public_key.to_checksum_address()
        keccak_hash = keccak.new(digest_bits=256)
        keccak_hash.update(address.encode())
        hash_msg = keccak_hash.digest()
        signature = privKey.sign_msg_hash(hash_msg)


        payload = self.makeJsonRpcRequest(API_DEL_ETH_ADDRESS, token)
        payload["params"]["address"]  = address
        payload["params"]["public_key"]  = self.remove0xHeader(privKey.public_key.to_hex())
        payload["params"]["signature"] = self.formSignature(signature.to_hex())
       
        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return False
        
        data = res.json()

        if data['id'] != payload['id']:
            return False
       
        if data["result"]["err_code"] == 0:
            return True
        else:
            return False

    """
        Deposit Etn Token from ERC20
    """
    async def deposit_token_async(self, token='',txhash=''):
         res = await asyncio.get_event_loop().run_in_executor(None, self.deposit_token,  token, txhash) 
         return res

    def deposit_token(self,token='', txhash=''):

        payload = self.makeJsonRpcRequest(API_DEPOSIT_TOKEN, token)
        payload["params"]["txhash"] = txhash

        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return False        
        
        data = res.json()

        if data['id'] != payload['id']:
            return False

        if data["result"]["err_code"] == 0:
            return True
        else:
            return False

    """
        Withdraw Etn Token to ERC20
    """
    async def withdraw_token_async(self, token='',ethaddress='',amount=0):
         res = await asyncio.get_event_loop().run_in_executor(None, self.withdraw_token,  token, ethaddress, amount) 
         return res

    def withdraw_token(self,token='', ethaddress='',amount=0):

        payload = self.makeJsonRpcRequest(API_WITHDRAW_TOKEN, token)
        payload["params"]["ethaddress"] = ethaddress
        payload["params"]["amount"] = amount

        res = requestsPost( self.config['api_end_point'], data=json.dumps(payload))

        if res.status_code != 200:
            return False        
        
        data = res.json()

        if data['id'] != payload['id']:
            return False

        if data["result"]["err_code"] == 0:
            return data["result"]["data"]["txhash"]
        else:
            return False



    def get_encoding(self, msg, from_encoding='base64', to_encoding='base58'):

        # Encoding check.

        if from_encoding == 'base64':
            missing_padding = len(msg) % 4
            if missing_padding != 0:
                msg += b'='* (4 - missing_padding)
            data = base64.b64decode(msg)
        elif from_encoding == 'base58':
            data = base58.b58decode(msg)
        else:
            return None

        if to_encoding == 'base64':
            return base64.b64encode(data)
        elif to_encoding == 'base58':
            return base58.b58encode(data)
        return None
