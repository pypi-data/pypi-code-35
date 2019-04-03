from rlp.sedes import (
    Serializable,
    CountableList,
    big_endian_int,
    binary
)
from rlp import encode as encode_rlp
from hashlib import blake2b
from eth_keys import keys
from utils import *


class Clause(Serializable):
    fields = [
        ('To', binary),  # b''
        ('Value', big_endian_int),
        ('Data', binary),  # b''
    ]

    def __init__(self, to='', value=0, data=''):
        super(Clause, self).__init__(decode_hex(to), value, decode_hex(data))


class Transaction(Serializable):
    fields = [
        ('ChainTag', big_endian_int),
        ('BlockRef', big_endian_int),
        ('Expiration', big_endian_int),
        ('Clauses', CountableList(Clause)),  # []
        ('GasPriceCoef', big_endian_int),
        ('Gas', big_endian_int),
        ('DependsOn', binary),  # b''
        ('Nonce', big_endian_int),
        ('Reserved', CountableList(object)),  # []
        ('Signature', binary),  # b''
    ]

    def __init__(self, chain_tag, blk_ref, *clauses):
        super(Transaction, self).__init__(chain_tag, blk_ref,
                                          (2 ** 32) - 1, clauses, 0, 3000000, b'', 0, [], b'')

    def sign(self, private_key):
        '''Sign this transaction with a private key.

        A potentially already existing signature would be overridden.
        '''
        h = blake2b(digest_size=32)
        h.update(encode_rlp(self, Transaction.exclude(['Signature'])))
        rawhash = h.digest()

        if private_key in (0, '', b'\x00' * 32, '0' * 64):
            raise Exception('Zero privkey cannot sign')

        if len(private_key) == 64:
            private_key = hexstr_to_bytes(private_key)  # we need a binary key
        pk = keys.PrivateKey(private_key)

        self.Signature = pk.sign_msg_hash(rawhash).to_bytes()

        return "0x{}".format(encode_hex(encode_rlp(self)))
