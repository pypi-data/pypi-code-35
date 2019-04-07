import decimal
import requests
import json

class BitSV:

    description = '''
        The BitSV wallet connects to the Bitcoin SV blockchain with the help of BitSV python library

        Dependencies:
        - bitsv : "pip install bitsv"
        - bcashaddress : "pip install cashaddress" (temporary)
    '''

    default_options = {}
    uses_secret_variables = ["BITSV_KEY"]

    def __init__(self):
        self.options = {}
        self.secrets = {}

    def start(self, log):
        import bitsv

        self.log = log
        self.bitsv = bitsv
        self.key = bitsv.Key(self.secrets['BITSV_KEY'])

        if self.key.address[:len("bitcoincash:")] == "bitcoincash:":
            import cashaddress
            self.address = cashaddress.convert.to_legacy_address(self.key.address)
        else:
            self.address = self.key.address

        self.broadcast_rawtx = bitsv.network.services.BitIndex.broadcast_rawtx

        

    def validate_options(self):
        pass

    def check_dependencies_missing(self):
        import bitsv
        import cashaddress

    satInB = decimal.Decimal(100000000)

    def checkBalance(self):
        '''Returns the available funds in the wallet'''
        return decimal.Decimal(int(self.key.get_balance('satoshi'))) / self.satInB

    def send(self, amount, address):
        '''Sends funds to the specified address'''
        sats = int(decimal.Decimal(amount) * self.satInB)
        tx = self.key.create_transaction([
            (address, sats, 'satoshi')
        ])
        result = self.broadcast_rawtx(tx)
        try:
            return result["data"]["txid"]
        except Exception:
            raise Exception(result["message"]["message"])


    def getReceiveAddress(self):
        '''Returns a public receiving address of this wallet'''
        return self.address

    def getLatestTransactions(self, numOfTransactions=10, transactionsToSkip=0):
        '''Returns a list containing the latest transactions of this wallet.
        Transactions are ordered by their recency (newest first, oldest last)
        'numOfTransactions' is the maximum number of transactions to return
        'transactionsToSkip' specifies how many (newer) transactions to skip, before getting the older ones

        Each transaction should be represented as a 'dict' like:

        {
            'amount': Decimal = the total sum of money transfered in this TX (positive number for receiving and negative otherwise)
            'time': int = epoch timestamp in seconds
            'id': string = the transaction id
            'confirmations': int = how many blocks confirm the transaction.
        }

        Different wallets can add additional values in the dictionary, but the listed ones are mandatory.'''
        
        transactionIds = self.key.get_transactions()

        fr = transactionsToSkip
        to = fr + numOfTransactions
        transactionIds = transactionIds[fr:to]
        
        transactions = [self.getTx(txid) for txid in transactionIds]
        return transactions

    def getTx(self, txid):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        r = requests.get('https://api.bitindex.network/api/v2/tx/' + str(txid), headers=headers)
        response = json.loads(r.content, parse_float=decimal.Decimal)['data']

        amount_out = sum([ vout['value'] if 'value' in vout else 0 for vout in response['vout'] ])

        return {
            'amount': amount_out,
            'time': response["time"],
            'id': txid,
            'confirmations': response["confirmations"],
        }