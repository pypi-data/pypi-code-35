# -*- coding: utf-8 -*-

import time
import re
import json
import logging
from web3 import Web3, HTTPProvider, IPCProvider, WebsocketProvider
from web3.contract import ConciseContract
from eth_account import Account
from eth_utils import add_0x_prefix, to_checksum_address, is_address, encode_hex

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console = logging.StreamHandler()
console.setFormatter(formatter)
log.addHandler(console)


def is_privatekey(key):
    """
    监测private key长度是否正确
    必须是64位的长度
    """
    import re
    prog = re.compile('^[a-zA-Z0-9]{64}$')
    tf = prog.match(key)
    return tf


class Contract(object):
    """
    基础协约
    定义一些基础的方法
    """
    _w3 = Web3()
    _provider = ''              # 哪种方式连接的以太坊
    _contract_address = ''      # 智能协约的address
    _abi = ''                   # 智能协约的abi
    _owner_private_key = ''     # 智能协约的创建者
    _operator_private_key = ''  # 智能协约的操作者
    _delegate_private_key = ''  # 代理账号的私钥

    def __init__(self, provider='http://localhost:7545', timeout=60, *args, **kwargs):
        self._provider = provider
        if re.match('^http://.*', provider):
            self._w3 = Web3(HTTPProvider(provider, request_kwargs={'timeout': timeout}))
        elif re.match('^ws://.*', provider):
            self._w3 = Web3(WebsocketProvider(provider))
        else:
            self._w3 = Web3(IPCProvider(provider))
        for k in kwargs:
            if k == 'contract_address':
                self._contract_address = kwargs[k]
            if k == 'abi':
                self._abi = list(kwargs[k])
            if k == 'owner_private_key':
                self._owner_private_key = kwargs[k]
            if k == 'operator_private_key':
                self._operator_private_key = kwargs[k]
            if k == 'delegate_private_key':
                self._delegate_private_key = kwargs[k]
        # print(type(self._abi))

    @property
    def w3(self):
        return self._w3

    @property
    def contract_address(self):
        return self._contract_address

    @contract_address.setter
    def contract_address(self, contract_address):
        self._contract_address = contract_address

    @property
    def abi(self):
        return self._abi

    @abi.setter
    def abi(self, abi):
        self._abi = abi

    @property
    def owner(self):
        return self._owner_private_key

    @owner.setter
    def owner(self, owner_private_key):
        self._owner_private_key = owner_private_key

    @property
    def operator(self):
        return self._operator_private_key

    @operator.setter
    def operator(self, operator_private_key):
        self._operator_private_key = operator_private_key

    # def wait_for_transaction_receipt(self, txid):
    #     web3 = self._w3.eth.waitForTransactionReceipt(txid)

    def check_receipts(self, txid):
        """
        根据交易id获得receipts
        :param txid: 交易ID
        :return:
        """
        try:
            # receipt = self._w3.eth.getTransactionReceipt(txid)
            receipt = self._w3.eth.waitForTransactionReceipt(txid)
        except Exception as e:
            print(e)
            receipt = None
        return receipt

    def wait_for_tx(self, txid, second=120):
        """等待交易完成"""
        import sys
        sec = 0
        timeout = False
        receipt = self.check_receipts(txid)
        while (receipt == None) or (receipt != None and receipt.blockHash == None):
            time.sleep(1)
            sec += 1
            print('.', end='')
            sys.stdout.flush()
            receipt = self.check_receipts(txid)
            if sec > second:
                timeout = True
                log.info('{}  {}\'s Transaction timeout'.format(txid,sec))
                log.info('Transaction timeout!')
                break
        print('seconds:[{}]'.format(sec))
        if receipt != None and receipt.blockHash != None:
            print('receipt: ' + str(dict(receipt)))
            return True, receipt
        return  False, receipt if timeout else True, receipt

    def get_address_nonce(self, address):
        """
        获得 address 对应的 nonce 值
        :param address:
        :return:
        """
        web3 = self._w3
        if is_address(address):
            nonce = web3.eth.getTransactionCount(to_checksum_address(address), block_identifier=web3.eth.defaultBlock)
        else:
            raise ValueError("%s is not a address" % address)
        return nonce

    def get_private_key_nonce(self, private_key):
        """
        获得 private_key 对应的 nonce 值
        :param private_key:
        :return:
        """
        address = self.private_key_to_address(private_key)
        return self.get_address_nonce(address)

    @staticmethod
    def private_key_to_address(private_key):
        """
        获得private_key对应的address(这个地址是checkSum的)
        :param private_key:
        :return: address
        """
        acct = Account.privateKeyToAccount(private_key)
        return acct.address

    @staticmethod
    def to_check_sum_address(address):
        """
        将address进行checkSum
        :param address:
        :return:
        """
        normal_address = add_0x_prefix(address)
        return Web3.toChecksumAddress(normal_address)

    def get_block(self):
        return self._w3.eth.getBlock()

    @property
    def block_number(self):
        return self._w3.eth.blockNumber

    @property
    def transaction(self, tx_hash):
        return self._w3.eth.getTransaction(tx_hash)

    @property
    def transaction_receipt(self, tx_hash):
        return self._w3.eth.getTransactionReceipt(tx_hash)

    def get_contract(self):
        """ 用于调用 function 进行写（会进行上链操作） """
        web3 = self._w3
        starcoin_address_checksum = self.to_check_sum_address(self._contract_address)
        contract = web3.eth.contract(abi=self._abi, address=starcoin_address_checksum)
        return contract

    def get_concise_contract(self):
        """ 用于读取本地状态数据的协约 """
        web3 = self._w3
        starcoin_address_checksum = self.to_check_sum_address(self._contract_address)
        contract = web3.eth.contract(abi=self._abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
        return contract

    def send_eth(self, sender_private_key, receiver_address, eth, gas=200000):
        """
        转eth
        :param sender_private_key: 发送者的私钥
        :param receiver_address: 接收者的address
        :param eth: 具体的ETH数量
        :param gas:
        :return:
        """
        web3 = self._w3
        nonce = self.get_private_key_nonce(sender_private_key)
        signed_txn = web3.eth.account.signTransaction(dict(
            nonce=nonce,
            gasPrice=web3.eth.gasPrice,
            gas=gas,
            to=web3.toChecksumAddress(receiver_address),
            value=eth,
            # value=20000 * 10 ** 18,
            data=b'',
        ),
            sender_private_key,
        )
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return tx_hash

    def call_function(self, contract_function, private_key, gas=100000000, gas_prise=100000):
        """
        调用协约的方法获得txid
        :param contract_function: 智能协约中对应的方法
        :param private_key: 签名用的private key
        :param gas:
        :param gas_prise:
        :return:
        """
        web3 = self._w3
        nonce = self.get_private_key_nonce(private_key)
        log.info('nonce:{}'.format(nonce))
        tx_info = contract_function.buildTransaction(
            {'nonce': nonce,
             'gasPrice': gas_prise,
             'gas': gas}
        )
        signed_txn = web3.eth.account.signTransaction(tx_info, private_key)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        tx_hash_hex = encode_hex(tx_hash)
        (tf, receipt) = self.wait_for_tx(tx_hash_hex)
        log.info(receipt)
        return tf, tx_hash

    def call_function_wait(self, contract_function, private_key, gas=100000000, gas_prise=100000):
        """
        调用协约的方法获得txid (会一直循环操作)
        如果pool里面已经有相同的txid，就会一直循环到下一个nonce值，在提交
        :param contract_function: 智能协约中对应的方法
        :param private_key: 签名用的private key
        :param gas:
        :param gas_prise:
        :return:
        """
        web3 = self._w3
        while True:
            try:
                nonce = self.get_private_key_nonce(private_key)
                log.info("nonce:{}".format(nonce))
                tx_info = contract_function.buildTransaction(
                    {'nonce': nonce,
                     'gasPrice': gas_prise,
                     'gas': gas}
                )
                signed_txn = web3.eth.account.signTransaction(tx_info, private_key)
                tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            except ValueError as e:
                json_str = str(e)
                log.info(json_str)
                error_msg = json.loads(json.dumps(eval(json_str)))
                code = error_msg['code']
                if code == -32010:
                    time.sleep(1)
                    continue
            break
        tx_hash_hex = encode_hex(tx_hash)
        receipt = self.wait_for_tx(tx_hash_hex)
        log.info(receipt)
        return tx_hash

    def __str__(self):
        return "connect provider : %s" % self._provider


class Cport(Contract):
    """
    Cport 相关的协约操作
    """
    def __init__(self, provider, timeout=60, *args, **kwargs):
        super(Cport, self).__init__(provider, timeout, *args, **kwargs)

    def example(self, operator_address):
        """ 例子1 """
        contract = self.get_contract()
        value = contract.functions.getOperator(operator_address).call()
        return value

    def example2(self, operator_address):
        """ 例子2 """
        concise_contract = self.get_concise_contract()
        value = concise_contract.getOperator(operator_address)
        return value

    def set_DID_Operator(self, operator_address):
        pass



    def change_owner(self, identity_address, new_owner_address):
        """
        调用Uport协约中的 changeOwner 方法
        :param identity_address: 参数1
        :param new_owner_address: 参数2
        :return:
        """
        contract = self.get_contract()
        uport_function = contract.functions.changeOwner(identity_address, new_owner_address)
        tx_hash = self.call_function(uport_function, self._operator_private_key)
        timeout = self.waitForTx(tx_hash)
        return not timeout

    def get_reward_pool(self):
        """
        获得协约里面的当日奖池的剩余
        """
        concise_contract = self.get_concise_contract()
        pool = int(concise_contract.getRewardPool() / 10000000000)
        return pool

    def set_operator(self, operator_address, value=1):
        """
        设置operator账号
        :param operator_address:
        :param value:
        :return:
        """
        contract = self.get_contract()
        function = contract.functions.setOperator(operator_address, value)
        tx_hash = self.call_function(function, self._owner_private_key)
        return encode_hex(tx_hash)

    def get_operator(self, operator_address):
        """
        确认一个账号是否是operator账号
        :param operator_address:
        :return: 1:是，0:否
        """
        contract = self.get_contract()
        value = contract.functions.getOperator(operator_address).call()
        # concise_contract = self.get_concise_contract()
        # value = concise_contract.getOperator(operator_address)
        return value

    def change_contract_owner(self, new_owner_address):
        """
        变更owner账号（只有协约的拥有者能够调用）
        :param new_owner_address:
        :return:
        """
        contract = self.get_contract()
        function = contract.functions.changeContractOwner(new_owner_address)
        tx_hash = self.call_function(function, self._owner_private_key)
        return encode_hex(tx_hash)

    def get_contract_owner(self):
        """
        获得协约的拥有者address
        :return: address  （hex）
        """
        concise_contract = self.get_concise_contract()
        value = concise_contract.getContractOwner()
        return value

    def set_delegate(self, attribute, delegate_address, value):
        """
        调用智能协约的：setDelegate 方法
        :param attribute:
        :param delegate_address:
        :param value:
        :return:
        """
        if not isinstance(value, int):
            raise ValueError('function:set_delegate(), value:[{0}] Incorrect parameter type'.format(value))
        contract = self.get_contract()
        function = contract.functions.setDelegate(attribute, delegate_address, value)
        tx_hash = self.call_function(function, self._operator_private_key)
        return encode_hex(tx_hash)

    def get_delegate(self):
        """
        调用智能协约的 getDelegate 方法
        :return:
        """
        concise_contract = self.get_concise_contract()
        value = concise_contract.getDelegate()
        return value

    def identity_owner(self, identity_address):
        """
        调用智能协约的 identityOwner 的方法
        :param identity_address:
        :return:
        """
        contract = self.get_contract()
        function = contract.functions.identityOwner(identity_address)
        tx_hash = self.call_function(function, self._operator_private_key)
        return encode_hex(tx_hash)

    def change_did_owner(self, identity_address, new_owner_address):
        """
        调用智能协约的 changeDIDOwner 方法
        :param identity_address:
        :param new_owner_address:
        :return:
        """
        contract = self.get_contract()
        function = contract.functions.changeDIDOwner(identity_address, new_owner_address)
        tx_hash = self.call_function(function, self._operator_private_key)
        return encode_hex(tx_hash)

    def check_signature(self, identity_address, sigV, sigR, sigS, hash):
        """
        调用智能协约的 checkSignature 方法
        :param identity_address:
        :param sigV:
        :param sigR:
        :param sigS:
        :param hash:
        :return:
        """
        contract = self.get_contract()
        function = contract.functions.setAttributeSigned(identity_address, sigV, sigR, sigS, hash)
        tx_hash = self.call_function(function, self._operator_private_key)
        return encode_hex(tx_hash)

    def set_attribute(self, identity_address, owner_address, name, value):
        """
        调用智能协约的 setAttribute 方法
        :param identity_address:
        :param owner_address:
        :param name:
        :param value:
        :return:
        """
        contract = self.get_contract()
        function = contract.functions.setAttribute(identity_address, owner_address, name, value)
        tx_hash = self.call_function(function, self._owner_private_key)
        # contract = self.get_concise_contract()
        # contract.functions.setAttribute(identity_address, owner_address, name, value).transact()
        return encode_hex(tx_hash)

    def confirm_attribute(self, identity, name, value):
        """
        调用智能协约的 confirmAttribute 方法
        :param identity:
        :param name:
        :param value:
        :return:
        """
        contract = self.get_contract()
        function = contract.functions.confirmAttribute(identity, name, value)
        # TODO: onlyDelegate 才能调用，需要添加一个delegate的账号权限到属性中
        tf, tx_hash = self.call_function(function, self._operator_private_key)
        return tf, encode_hex(tx_hash)


class StarCoin(Contract):
    """
    星钻 相关的协约操作
    """
    def __init__(self, provider, timeout=60):
        super(StarCoin, self).__init__(provider, timeout)

    def get_reward_pool(self):
        """ 获得协约里面的当日奖池的剩余 """
        web3 = self._w3
        starcoin_address_checksum = self.to_check_sum_address(self._contract_address)
        starcoin = web3.eth.contract(
            abi=self._abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
        pool = int(starcoin.getRewardPool() / 10000000000)
        return pool

#     def get_daily_reware_pool(web3, starcoin_address, abi):
#         """ 获得协约里面的当日奖池的剩余 """
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = int(starcoin2.getDailyRewardPool() / 10000000000)
#         return pool
#
#     def get_operator_pool(web3, starcoin_address, abi):
#         """ 获得协约里面的 operator 池的剩余 """
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = int(starcoin2.getOperatorPool() / 10000000000)
#         return pool
#
#     def get_airdrop_pool(web3, starcoin_address, abi):
#         """ 获得协约里面的 空投 池的剩余 """
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = int(starcoin2.getAirDropPool() / 10000000000)
#         return pool
#
#     def get_centrabank_pool(web3, starcoin_address, abi):
#         """ 获得协约里面的 空投 池的剩余 """
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = int(starcoin2.getCentralBank() / 10000000000)
#         return pool
#
#     def get_star_pool(web3, starcoin_address, abi):
#         """ 获得协约里面的 空投 池的剩余 """
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = int(starcoin2.getStarPool() / 10000000000)
#         return pool
#
#     def depositToOperatorPool(web3, starcoin_address, abi, coin):
#         """ 存款到运营账号 """
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = int(starcoin2.getStarPool() / 10000000000)
#         return pool
#
#     def depositToRewardPool(web3, starcoin_address, abi, coin):
#         """ 存款到挖矿账号 """
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, starcoin_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         txid = starcoin2.depositToRewardPool(coin)
#         timeout = waitForTx(web3, txid)
#         return not timeout
#
#     def get_eth_balances(web3, search_address):
#         """ 获得地址对应的以太坊余额 """
#         search_address_checksum = utils.pack_address_checksum(web3, search_address)
#         eth_sum = web3.eth.getBalance(search_address_checksum)
#         return eth_sum
#
#
#
#     def addOperator(contract_address, abi, operator_address_pri, role):
#         """
#             添加operator账号到协约中
#             给指定的协约添加operator账号（使用协约部署账号操作）
#         :param contract_address:
#         :param abi:
#         :param operator_address:
#         :param role:  "airDropPool","rewardPool","centralBank","operatorPool","all"
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         # operator_address_pub = '0x' + encode_hex(privtoaddr(operator_address_pri))
#         # operator_address = utils.pack_address_checksum(web3, operator_address_pub)
#
#         operator_address = web3.toChecksumAddress(privtoaddr(operator_address_pri))
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#
#         pub_key = privtoaddr(settings.DEPLOY_CONTRACT_ADDRESS)
#         print(web3.toChecksumAddress(pub_key))
#         contract2 = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         print(contract2.owner())
#         operations = []
#         if role == 'all':
#             operations.append(contract.functions.setOpsForAirDropPool(operator_address, 1))
#             operations.append(contract.functions.setOpsForRewardPool(operator_address, 1))
#             operations.append(contract.functions.setOpsForCentralBank(operator_address, 1))
#             operations.append(contract.functions.setOpsForOperatorPool(operator_address, 1))
#         elif role == 'airDropPool':
#             operations.append(contract.functions.setOpsForAirDropPool(operator_address, 1))
#         elif role == 'rewardPool':
#             operations.append(contract.functions.setOpsForRewardPool(operator_address, 1))
#         elif role == 'centralBank':
#             operations.append(contract.functions.setOpsForCentralBank(operator_address, 1))
#         elif role == 'operatorPool':
#             operations.append(contract.functions.setOpsForOperatorPool(operator_address, 1))
#         sucess = True
#         for function in operations:
#             txid = send_tx(function, settings.DEPLOY_CONTRACT_ADDRESS)
#             timeout = waitForTx(txid)
#             if timeout:
#                 sucess = False
#         txid = send_eth(settings.DEPLOY_CONTRACT_ADDRESS, operator_address, 1000 * 10 ** 18)
#         timeout = waitForTx(txid)
#         if timeout:
#             sucess = False
#         eth = web3.eth.getBalance(operator_address)
#         print(operator_address + "   =    " + str(eth))
#         return sucess
#
#     def getOperator(contract_address, abi):
#         """
#             获得协约中的所有operator账号
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         starcoin2 = web3.eth.contract(
#             abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         accounts = starcoin2.getAccountOperator()
#         logger.info(accounts)
#         from ethereum.utils import privtoaddr
#         sender_private_key = '68aab5eb6d0f5e04c17db5108165eb23d03cf1446b3d848a3c2220e61024a6da'
#         sender_address = web3.toChecksumAddress(privtoaddr(sender_private_key))
#         logger.info(sender_address)
#
#     def allocateDailyRewardPool(contract_address, abi, operator_address_pri, coin):
#         """
#         给矿池打钱
#         :param contract_address:
#         :param abi:
#         :param operator_address:
#         :param coin: 需要转的钱数  2000 * 10 ** 10
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#         function = contract.functions.allocateDailyRewardPool(int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_address_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
#     def depositToRewardPool(contract_address, abi, operator_address_pri, coin):
#         """
#         发起者 存款到挖矿账户
#         :param contract_address: 协约的address
#         :param abi:
#         :param operator_address: 发起者的private key
#         :param coin: 需要转的钱数  2000 * 10 ** 10
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#         function = contract.functions.depositToRewardPool(int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_address_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
#     def depositToAirDropPool(contract_address, abi, operator_address_pri, coin):
#         """
#         发起者 存款到空投账户
#         :param contract_address: 协约的address
#         :param abi:
#         :param operator_address: 发起者的private key
#         :param coin: 需要转的钱数  2000 * 10 ** 10
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#         function = contract.functions.depositToAirDropPool(int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_address_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
#     def depositToStarPool(contract_address, abi, operator_address_pri, coin):
#         """
#         发起者 存款到明星账户
#         :param contract_address: 协约的address
#         :param abi:
#         :param operator_address: 发起者的private key
#         :param coin: 需要转的钱数  2000 * 10 ** 10
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#         function = contract.functions.depositToStarPool(int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_address_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
#     def depositToCentralBank(contract_address, abi, operator_address_pri, coin):
#         """
#         发起者 存款到中央银行
#         :param contract_address: 协约的address
#         :param abi:
#         :param operator_address: 发起者的private key
#         :param coin: 需要转的钱数  2000 * 10 ** 10
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=depositToCentralBank)
#         function = contract.functions.depositToStarPool(int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_address_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
#     def getDailyRewardPool(contract_address, abi):
#         """
#         获得dailyRewardPool里面钱的数量
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getDailyRewardPool()
#         return pool
#
#     def getCentralBank(contract_address, abi):
#         """
#         获得getCentralBank里面钱的数量
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getCentralBank()
#         return pool
#
#     def getAirDropPool(contract_address, abi):
#         """
#         获得getAirDropPool里面钱的数量
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getAirDropPool()
#         return pool
#
#     def getRewardPool(contract_address, abi):
#         """
#         获得getRewardPool里面钱的数量
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getRewardPool()
#         return pool
#
#     def getOperatorPool(contract_address, abi):
#         """
#         获得getOperatorPool里面钱的数量
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getOperatorPool()
#         return pool
#
#     def getFansLockDuration(contract_address, abi):
#         """
#         获得 getFansLockDuration 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getFansLockDuration()
#         return pool
#
#     def getRewardScale(contract_address, abi):
#         """
#         获得 getRewardScale 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getRewardScale()
#         return pool
#
#     def getInitStarCoin(contract_address, abi):
#         """
#         获得 getInitStarCoin 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getInitStarCoin()
#         return pool
#
#     def getInitEthForFans(contract_address, abi):
#         """
#         获得 getInitEthForFans 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getInitEthForFans()
#         return pool
#
#     def getDailyBlockNumber(contract_address, abi):
#         """
#         获得 getDailyBlockNumber 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getDailyBlockNumber()
#         return pool
#
#     def getDepositAccount(contract_address, abi):
#         """
#         获得 getDepositAccount 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getDepositAccount()
#         return pool
#
#     def getLastUpdateMaskBlockNum(contract_address, abi):
#         """
#         获得 getLastUpdateMaskBlockNum 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getLastUpdateMaskBlockNum()
#         return pool
#
#     def getCurrentMask(contract_address, abi):
#         """
#         获得 getCurrentMask 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getCurrentMask()
#         return pool
#
#     def getMinimumDeposit(contract_address, abi):
#         """
#         获得 getMinimumDeposit 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getMinimumDeposit()
#         return pool
#
#     def getMaximumDeposit(contract_address, abi):
#         """
#         获得 getMaximumDeposit 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getMaximumDeposit()
#         return pool
#
#     def getDailyLuckyNumber(contract_address, abi):
#         """
#         获得 getDailyLuckyNumber 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getDailyLuckyNumber()
#         return pool
#
#     def getDepositAccount(contract_address, abi):
#         """
#         获得 getDepositAccount 里面的数据
#         :param contract_address:
#         :param abi:
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum, ContractFactoryClass=ConciseContract)
#         pool = contract.getDepositAccount()
#         return pool
#
#     def transferFromOperatorPool(contract_address, abi, operator_pri, receiver_add, coin):
#         """
#         从运营账号转钱到指定的账号
#         :param contract_address: 协约地址
#         :param abi:
#         :param operator_pri: operator账号的private key。只有private key 才能签名交易
#         :param receiver_add: 接收者的address
#         :param coin: 钱数
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         receiver_address_checksum = utils.pack_address_checksum(web3, receiver_add)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#         function = contract.functions.transferFromOperatorPool(receiver_address_checksum, int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
#     def transferFromCentralBank(contract_address, abi, operator_pri, receiver_add, coin):
#         """
#         从中央银行转钱到指定的账号
#         :param contract_address: 协约地址
#         :param abi:
#         :param operator_pri: operator账号的private key。只有private key 才能签名交易
#         :param receiver_add: 接收者的address
#         :param coin: 钱数
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         receiver_address_checksum = utils.pack_address_checksum(web3, receiver_add)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#         function = contract.functions.transferFromCentralBank(receiver_address_checksum, int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
#     def transferFromStarPool(contract_address, abi, operator_pri, receiver_add, coin):
#         """
#         从明星账号转钱到指定的账号
#         :param contract_address: 协约地址
#         :param abi:
#         :param operator_pri: operator账号的private key。只有private key 才能签名交易
#         :param receiver_add: 接收者的address
#         :param coin: 钱数
#         :return:
#         """
#         # 连接rpc
#         web3 = getWeb3()
#         starcoin_address_checksum = utils.pack_address_checksum(web3, contract_address)
#         receiver_address_checksum = utils.pack_address_checksum(web3, receiver_add)
#         contract = web3.eth.contract(abi=abi, address=starcoin_address_checksum)
#         function = contract.functions.transferFromStarPool(receiver_address_checksum, int(coin) * 10 ** 10)
#         txid = send_tx(function, operator_pri)
#         timeout = waitForTx(txid)
#         return not timeout
#
# def pack_address_checksum(web3, address):
#     """对于address没有添加0x前缀，自动添加, 然后在checksum """
#     p_address = pack_address(address)
#     checksum_address = web3.toChecksumAddress(p_address)
#     return checksum_address
#
#
# def get_eth_nonce(web3, operator_address_pri):
#     """ 获得nonce值 """
#     # 连接以太坊
#     web3 = getWeb3()
#     operator_address = eth_utils.encode_hex(eth_utils.privtoaddr(operator_address_pri))
#     operator_address_checksum = utils.pack_address_checksum(web3, operator_address)
#     nonce = web3.eth.getTransactionCount(operator_address_checksum, block_identifier=web3.eth.defaultBlock)
#     return nonce





