# -*- coding: utf-8 -*-

from web3 import Web3, HTTPProvider
import setting
import time
from logger import logger
from web3.contract import ConciseContract
from ethereum import utils as eth_utils
from ethereum.utils import encode_hex, privtoaddr

def getWeb3():
    # 连接rpc
    web3 = Web3(HTTPProvider(setting.ETH_URL, request_kwargs={'timeout': setting.ETH_TIMEOUT}))
    return web3


def checkReceipts(txid):
    """获取交易收据"""
    try:
        web3 = getWeb3()
        receipt = web3.eth.getTransactionReceipt(txid)
    except Exception as e:
        receipt = None
    return receipt


def waitForTx(txid, second=120):
    """等待交易完成"""
    sec = 0
    timeout = False
    web3 = getWeb3()
    receipt = checkReceipts(txid)
    logger.info(receipt)
    while (receipt == None) or (receipt != None and receipt.blockHash == None):
        # while receipt == None:
        time.sleep(3)
        sec += 1
        print(str(sec) + 's', end='')
        receipt = checkReceipts(txid)
        if sec > second:
            timeout = True
            print(str(txid) + '  ' + str(sec) + 's Transaction timeout')
            print('Transaction timeout!')
            break
    if receipt != None and receipt.blockHash != None:
        print('receipt:     ' + str(dict(receipt)))
    return timeout

def is_privatekey(key):
    """
    监测private key长度是否正确
    必须是64位的长度
    """
    import re
    prog = re.compile('^[a-zA-Z0-9]{64}$')
    tf = prog.match(key)
    logger.info(tf)
    return tf

def is_publickey(key):
    """
    判断是否为公钥
    :param key:
    :return:
    """
    # TODO: 需要实现
    pass

def pack_address(address):
    """对于address没有添加0x前缀，自动添加"""
    if '0x' == address[0:2]:
        return address
    else:
        return '0x' + address

def pack_address_checksum(web3, address):
    """对于address没有添加0x前缀，自动添加, 然后在checksum """
    p_address = pack_address(address)
    checksum_address = web3.toChecksumAddress(p_address)
    return checksum_address


def get_eth_nonce(web3, operator_address_pri):
    """ 获得nonce值 """
    # 连接以太坊
    web3 = getWeb3()
    operator_address = eth_utils.encode_hex(eth_utils.privtoaddr(operator_address_pri))
    operator_address_checksum = utils.pack_address_checksum(web3, operator_address)
    nonce = web3.eth.getTransactionCount(operator_address_checksum, block_identifier=web3.eth.defaultBlock)
    return nonce


def get_reward_pool(web3, starcoin_address, abi):
    """ 获得协约里面的当日奖池的剩余 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = int(starcoin2.getRewardPool() / 10000000000)
    return pool


def get_daily_reware_pool(web3, starcoin_address, abi):
    """ 获得协约里面的当日奖池的剩余 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = int(starcoin2.getDailyRewardPool() / 10000000000)
    return pool


def get_operator_pool(web3, starcoin_address, abi):
    """ 获得协约里面的 operator 池的剩余 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = int(starcoin2.getOperatorPool() / 10000000000)
    return pool


def get_airdrop_pool(web3, starcoin_address, abi):
    """ 获得协约里面的 空投 池的剩余 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = int(starcoin2.getAirDropPool() / 10000000000)
    return pool


def get_centrabank_pool(web3, starcoin_address, abi):
    """ 获得协约里面的 空投 池的剩余 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = int(starcoin2.getCentralBank() / 10000000000)
    return pool


def get_star_pool(web3, starcoin_address, abi):
    """ 获得协约里面的 空投 池的剩余 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = int(starcoin2.getStarPool() / 10000000000)
    return pool


def depositToOperatorPool(web3, starcoin_address, abi, coin):
    """ 存款到运营账号 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = int(starcoin2.getStarPool() / 10000000000)
    return pool


def depositToRewardPool(web3, starcoin_address, abi, coin):
    """ 存款到挖矿账号 """
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    txid = starcoin2.depositToRewardPool(coin)
    timeout = waitForTx(web3, txid)
    return not timeout


def get_eth_balances(web3, search_address):
    """ 获得地址对应的以太坊余额 """
    search_address_checksum = utils.pack_address_checksum(web3, search_address)
    eth_sum = web3.eth.getBalance(search_address_checksum)
    return eth_sum

def send_eth(sender_pri, receiver_pub, eth):
    """
    转eth
    :param sender_pri: 发送者的私钥
    :param receiver_pub: 接收者的公钥address
    :param eth: 具体的ETH数量 需要乘以 10 ** 18
    :return:
    """
    web3 = getWeb3()
    pub_key = privtoaddr(sender_pri)
    nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(pub_key))
    signed_txn = web3.eth.account.signTransaction(dict(
        nonce=nonce,
        gasPrice=web3.eth.gasPrice,
        gas=settings.GAS,
        to=web3.toChecksumAddress(receiver_pub),
        value=eth,
        # value=20000 * 10 ** 18,
        data=b'',
        ),
        sender_pri,
    )
    tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return tx_hash


def send_tx(func, private_key):
    """
    调用协约的方法获得txid
    :param func:
    :param private_key:
    :return:
    """
    web3 = getWeb3()
    pub_key = privtoaddr(private_key)
    nonce = web3.eth.getTransactionCount(web3.toChecksumAddress(pub_key))
    tx_info = func.buildTransaction(
        {'nonce': nonce,
         'gasPrice': settings.GAS_PRISE, 'gas': settings.GAS})
    tx = web3.eth.account.signTransaction(tx_info, private_key)
    tx_hash = web3.eth.sendRawTransaction(encode_hex(tx['rawTransaction']))
    logger.info(tx_hash)
    return tx_hash

def addOperator(contract_address, abi, operator_address_pri, role):
    """
        添加operator账号到协约中
        给指定的协约添加operator账号（使用协约部署账号操作）
    :param contract_address:
    :param abi:
    :param operator_address:
    :param role:  "airDropPool","rewardPool","centralBank","operatorPool","all"
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    # operator_address_pub = '0x' + encode_hex(privtoaddr(operator_address_pri))
    # operator_address = utils.pack_address_checksum(web3, operator_address_pub)

    operator_address = web3.toChecksumAddress(privtoaddr(operator_address_pri))
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)

    pub_key = privtoaddr(settings.DEPLOY_CONTRACT_ADDRESS)
    print(web3.toChecksumAddress(pub_key))
    contract2 = web3.eth.contract(abi=abi, address=starcoin_address_checksum,  ContractFactoryClass=ConciseContract)
    print(contract2.owner())
    operations = []
    if role == 'all':
        operations.append(contract.functions.setOpsForAirDropPool(operator_address, 1))
        operations.append(contract.functions.setOpsForRewardPool(operator_address, 1))
        operations.append(contract.functions.setOpsForCentralBank(operator_address, 1))
        operations.append(contract.functions.setOpsForOperatorPool(operator_address, 1))
    elif role == 'airDropPool':
        operations.append(contract.functions.setOpsForAirDropPool(operator_address, 1))
    elif role == 'rewardPool':
        operations.append(contract.functions.setOpsForRewardPool(operator_address, 1))
    elif role == 'centralBank':
        operations.append(contract.functions.setOpsForCentralBank(operator_address, 1))
    elif role == 'operatorPool':
        operations.append(contract.functions.setOpsForOperatorPool(operator_address, 1))
    sucess = True
    for function in operations:
        txid = send_tx(function, settings.DEPLOY_CONTRACT_ADDRESS)
        timeout = waitForTx(txid)
        if timeout:
            sucess = False
    txid = send_eth(settings.DEPLOY_CONTRACT_ADDRESS, operator_address, 1000 * 10 ** 18)
    timeout = waitForTx(txid)
    if timeout:
        sucess = False
    eth = web3.eth.getBalance(operator_address)
    print(operator_address + "   =    " + str(eth))
    return sucess


def getOperator(contract_address, abi):
    """
        获得协约中的所有operator账号
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    starcoin2 = web3.eth.contract(
        abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    accounts = starcoin2.getAccountOperator()
    logger.info(accounts)
    from ethereum.utils import privtoaddr
    sender_private_key = '68aab5eb6d0f5e04c17db5108165eb23d03cf1446b3d848a3c2220e61024a6da'
    sender_address = web3.toChecksumAddress(privtoaddr(sender_private_key))
    logger.info(sender_address)

def allocateDailyRewardPool(contract_address, abi, operator_address_pri, coin):
    """
    给矿池打钱
    :param contract_address:
    :param abi:
    :param operator_address:
    :param coin: 需要转的钱数  2000 * 10 ** 10
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
    function = contract.functions.allocateDailyRewardPool(int(coin) * 10 ** 10)
    txid = send_tx(function, operator_address_pri)
    timeout = waitForTx(txid)
    return not timeout

def depositToRewardPool(contract_address, abi, operator_address_pri, coin):
    """
    发起者 存款到挖矿账户
    :param contract_address: 协约的address
    :param abi:
    :param operator_address: 发起者的private key
    :param coin: 需要转的钱数  2000 * 10 ** 10
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
    function = contract.functions.depositToRewardPool(int(coin) * 10 ** 10)
    txid = send_tx(function, operator_address_pri)
    timeout = waitForTx(txid)
    return not timeout

def depositToAirDropPool(contract_address, abi, operator_address_pri, coin):
    """
    发起者 存款到空投账户
    :param contract_address: 协约的address
    :param abi:
    :param operator_address: 发起者的private key
    :param coin: 需要转的钱数  2000 * 10 ** 10
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
    function = contract.functions.depositToAirDropPool(int(coin) * 10 ** 10)
    txid = send_tx(function, operator_address_pri)
    timeout = waitForTx(txid)
    return not timeout

def depositToStarPool(contract_address, abi, operator_address_pri, coin):
    """
    发起者 存款到明星账户
    :param contract_address: 协约的address
    :param abi:
    :param operator_address: 发起者的private key
    :param coin: 需要转的钱数  2000 * 10 ** 10
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
    function = contract.functions.depositToStarPool(int(coin) * 10 ** 10)
    txid = send_tx(function, operator_address_pri)
    timeout = waitForTx(txid)
    return not timeout

def depositToCentralBank(contract_address, abi, operator_address_pri, coin):
    """
    发起者 存款到中央银行
    :param contract_address: 协约的address
    :param abi:
    :param operator_address: 发起者的private key
    :param coin: 需要转的钱数  2000 * 10 ** 10
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=depositToCentralBank)
    function = contract.functions.depositToStarPool(int(coin) * 10 ** 10)
    txid = send_tx(function, operator_address_pri)
    timeout = waitForTx(txid)
    return not timeout

def getDailyRewardPool(contract_address, abi):
    """
    获得dailyRewardPool里面钱的数量
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getDailyRewardPool()
    return pool

def getCentralBank(contract_address, abi):
    """
    获得getCentralBank里面钱的数量
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getCentralBank()
    return pool

def getAirDropPool(contract_address, abi):
    """
    获得getAirDropPool里面钱的数量
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getAirDropPool()
    return pool

def getRewardPool(contract_address, abi):
    """
    获得getRewardPool里面钱的数量
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getRewardPool()
    return pool

def getOperatorPool(contract_address, abi):
    """
    获得getOperatorPool里面钱的数量
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getOperatorPool()
    return pool

def getFansLockDuration(contract_address, abi):
    """
    获得 getFansLockDuration 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getFansLockDuration()
    return pool

def getRewardScale(contract_address, abi):
    """
    获得 getRewardScale 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getRewardScale()
    return pool

def getInitStarCoin(contract_address, abi):
    """
    获得 getInitStarCoin 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getInitStarCoin()
    return pool

def getInitEthForFans(contract_address, abi):
    """
    获得 getInitEthForFans 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getInitEthForFans()
    return pool

def getDailyBlockNumber(contract_address, abi):
    """
    获得 getDailyBlockNumber 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getDailyBlockNumber()
    return pool

def getDepositAccount(contract_address, abi):
    """
    获得 getDepositAccount 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getDepositAccount()
    return pool

def getLastUpdateMaskBlockNum(contract_address, abi):
    """
    获得 getLastUpdateMaskBlockNum 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getLastUpdateMaskBlockNum()
    return pool

def getCurrentMask(contract_address, abi):
    """
    获得 getCurrentMask 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getCurrentMask()
    return pool

def getMinimumDeposit(contract_address, abi):
    """
    获得 getMinimumDeposit 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getMinimumDeposit()
    return pool

def getMaximumDeposit(contract_address, abi):
    """
    获得 getMaximumDeposit 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getMaximumDeposit()
    return pool

def getDailyLuckyNumber(contract_address, abi):
    """
    获得 getDailyLuckyNumber 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getDailyLuckyNumber()
    return pool

def getDepositAccount(contract_address, abi):
    """
    获得 getDepositAccount 里面的数据
    :param contract_address:
    :param abi:
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
    pool = contract.getDepositAccount()
    return pool

def transferFromOperatorPool(contract_address, abi, operator_pri, receiver_add, coin):
    """
    从运营账号转钱到指定的账号
    :param contract_address: 协约地址
    :param abi:
    :param operator_pri: operator账号的private key。只有private key 才能签名交易
    :param receiver_add: 接收者的address
    :param coin: 钱数
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    receiver_address_checksum = utils.pack_address_checksum(web3, receiver_add)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
    function = contract.functions.transferFromOperatorPool(receiver_address_checksum, int(coin) * 10 ** 10)
    txid = send_tx(function, operator_pri)
    timeout = waitForTx(txid)
    return not timeout

def transferFromCentralBank(contract_address, abi, operator_pri, receiver_add, coin):
    """
    从中央银行转钱到指定的账号
    :param contract_address: 协约地址
    :param abi:
    :param operator_pri: operator账号的private key。只有private key 才能签名交易
    :param receiver_add: 接收者的address
    :param coin: 钱数
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    receiver_address_checksum = utils.pack_address_checksum(web3, receiver_add)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
    function = contract.functions.transferFromCentralBank(receiver_address_checksum, int(coin) * 10 ** 10)
    txid = send_tx(function, operator_pri)
    timeout = waitForTx(txid)
    return not timeout

def transferFromStarPool(contract_address, abi, operator_pri, receiver_add, coin):
    """
    从明星账号转钱到指定的账号
    :param contract_address: 协约地址
    :param abi:
    :param operator_pri: operator账号的private key。只有private key 才能签名交易
    :param receiver_add: 接收者的address
    :param coin: 钱数
    :return:
    """
    # 连接rpc
    web3 = getWeb3()
    starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
    receiver_address_checksum = utils.pack_address_checksum(web3, receiver_add)
    contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
    function = contract.functions.transferFromStarPool(receiver_address_checksum, int(coin) * 10 ** 10)
    txid = send_tx(function, operator_pri)
    timeout = waitForTx(txid)
    return not timeout


