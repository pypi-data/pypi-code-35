#!/usr/bin/env python
# -*- coding: utf-8 -*-

PATH = ''
VAR = {
    # 存放了相关的配置信息
    'MYSQL_TABLE_PRE': 'cp',
}



import configparser
from oracle import utils
# from oracle.database.dbs import query_keys, query_contract
# from oracle.database.modles import db
import json


def read_config(file='/etc/oracle.conf'):
    """
    读取配置文件的信息到 全局变量
    :param file: 配置文件的路径
    :return:
    """
    # 声明全局变量，才能修改数据
    global ETH_PORT, ETH_IP, ETH_URL, ETH_TIMEOUT
    global MYSQL_USER, MYSQL_PASSWORD, MYSQL_SCHEMA, MYSQL_PORT, MYSQL_IP, MYSQL_CHARSET

    config = configparser.RawConfigParser()
    config.read(file, encoding='utf8')
    # 读取 section=mysql 的配置信息
    MYSQL_USER = config.get('mysql', 'user')
    MYSQL_PASSWORD = config.get('mysql', 'password')
    MYSQL_SCHEMA = config.get('mysql', 'schema')
    MYSQL_PORT = config.getint('mysql', 'port')
    MYSQL_IP = config.get('mysql', 'ip')
    MYSQL_CHARSET = config.get('mysql', 'charset')

    # 读取 section=eth 的配置细信息
    ETH_PORT = config.getint('eth', 'port')
    ETH_IP = config.get('eth', 'ip')
    ETH_TIMEOUT = config.getint('eth', 'timeout')

    # 读取机器相关的配置信息
    MACHINE_FILE = config.get('common', 'machine_file')


def read_config2(file='/etc/oracle.conf'):
    """
    读取配置文件的信息到 VAR 变量
    :param file: 配置文件的路径
    :return:
    """
    config = configparser.RawConfigParser()
    config.read(file, encoding='utf8')

    # 读取 section=mysql 的配置信息
    VAR['MYSQL_USER'] = config.get('mysql', 'user')
    VAR['MYSQL_PASSWORD'] = config.get('mysql', 'password')
    VAR['MYSQL_SCHEMA'] = config.get('mysql', 'schema')
    VAR['MYSQL_PORT'] = config.getint('mysql', 'port')
    VAR['MYSQL_IP'] = config.get('mysql', 'ip')
    VAR['MYSQL_CHARSET'] = config.get('mysql', 'charset')
    VAR['MAX_CONNECTION'] = config.getint('mysql', 'max_connection')
    VAR['STALE_TIMEOUT'] = config.getint('mysql', 'stale_timeout')

    # 读取 机器相关的信息
    VAR['MACHINE_FILE'] = config.get('common', 'machine_file')
    VAR['MACHINE_ID'] = utils.get_machine_key(VAR['MACHINE_FILE'])

    # 初始化数据库，并且从数据库中获得private key信息
    from oracle.database.modles import db
    db.init(
        VAR['MYSQL_SCHEMA'],
        host=VAR['MYSQL_IP'],
        user=VAR['MYSQL_USER'],
        password=VAR['MYSQL_PASSWORD'],
        charset=VAR['MYSQL_CHARSET'],
        max_connections=VAR['MAX_CONNECTION'],
        stale_timeout=VAR['STALE_TIMEOUT'])
    from oracle.database.dbs import query_keys, query_contract
    key = query_keys(VAR['MACHINE_ID'])
    VAR['USER_PRIVATE_KEY'] = key.private_key
    VAR['USER_ADDRESS'] = key.address

    contract = query_contract()
    VAR['CONTRACT_ADDRESS'] = contract.contract_address
    # VAR['CONTRACT_ABI'] = contract.abi
    json_obj = json.loads(contract.abi)
    VAR['CONTRACT_ABI'] = json_obj['abi']

    # 读取 section=eth 的配置信息
    VAR['ETH_PROVIDER'] = config.get('eth', 'provider')
    VAR['ETH_TIMEOUT'] = config.getint('eth', 'timeout')
    VAR['CONTRACT_ADDRESS'] = config.get('eth', 'address')
    VAR['ARMY_PRIVATEKEY'] = config.get('eth', 'army_privatekey')
    VAR['OPERATOR_PRIVATEKEY'] = config.get('eth', 'operator_privatekey')
    VAR['DELEGATE_PRIVATEKEY'] = config.get('eth', 'delegate_privatekey')

    # 读取 section=common 的配置信息
    VAR['BLOCKNUM_CACHE_FILE'] = config.get('common', 'blocknum_cache_file')
    VAR['ARMY_BLOCKNUM_CACHE_FILE'] = config.get('common', 'army_blocknum_cache_file')
    VAR['ORGANIZATION_BLOCKNUM_CACHE_FILE'] = config.get('common', 'organization_blocknum_cache_file')
    VAR['ContractOwnerChange'] = config.get('common', 'ContractOwnerChange')
    VAR['DIDOwnerChanged'] = config.get('common', 'DIDOwnerChanged')
    VAR['DIDDelegateChanged'] = config.get('common', 'DIDDelegateChanged')
    VAR['DIDAttributeChange'] = config.get('common', 'DIDAttributeChange')
    VAR['DIDAttributeConfirmed'] = config.get('common', 'DIDAttributeConfirmed')
    VAR['BLOCKNUM_INC'] = config.getint('common', 'blocknum_inc')
    VAR['IDENTITY'] = config.get('common', 'identity')

    # 读取 section=redis 的配置信息
    VAR['REDIS_IP'] = config.get('redis', 'ip')
    VAR['REDIS_PORT'] = config.get('redis', 'port')
    VAR['REDIS_DATABASE'] = config.get('redis', 'database')
    VAR['REDIS'] = 'redis://{}:{}/1'.format(VAR['REDIS_IP'], VAR['REDIS_PORT'])

    # # 修改celery的配置
    # from oracle.tasks import app
    # app.conf.update(
    #     result_backend=VAR['REDIS'],
    #     broker_url=VAR['REDIS'],
    # )

    # 读取 section=wechat 的配置信息
    VAR['WECHAT_APPID'] = config.get('wechat', 'appid')
    VAR['WECHAT_SECRET'] = config.get('wechat', 'secret')









