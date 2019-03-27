#!/usr/bin/env python
# -*- coding: utf-8 -*-

from plyvel import DB
from . import utils
import logging


class Blockchain:

    @staticmethod
    def _get_block_key(height, prev_hash):
        return f"block_{height}_{prev_hash}"

    def __init__(self, chain_dir='./chaindata', signature_checker=None):
        self._db = DB(f'{chain_dir}', create_if_missing=True)
        if signature_checker:
            self.signature_checker = signature_checker
        self._write_batch = None

    def put(self, key, value):
        self._put(f'meta_{key}', value)

    def get(self, key):
        return self._get(f'meta_{key}')

    def add_block(self, block_dict):
        self.begin_transaction()
        height = self._increment_height()
        if self.get_block_by_hash(block_dict['hash']):
            raise PermissionError
        if not self._prev_hash_is_correct(height, block_dict['prev_hash']):
            raise PermissionError
        if not self._signature_is_valid(block_dict):
            raise PermissionError
        key = self._get_block_key(height, block_dict['hash'])
        self._put(key, block_dict) # height, block_hash -> block_dict
        self._put(height, block_dict['hash']) # height -> block_hash
        self._put(block_dict['hash'], height) # block_hash -> height
        self.commit()

    def get_block_by_height(self, height):
        block_hash = utils.bytes_to_str(self._get(str(height)))
        return self._get_block(height, block_hash)

    def get_block_by_hash(self, block_hash):
        height = utils.bytes_to_int(self._get(block_hash))
        return self._get_block(height, block_hash)

    def get_block_hash_by_height(self, height):
        return utils.bytes_to_str(self._get(height))

    def get_block_height_by_hash(self, block_hash):
        return utils.bytes_to_int(self._get(block_hash))

    def get_height(self):
        height = utils.bytes_to_int(self._get('height'))
        return height

    def print_chain(self):
        for key, value in self._db.iterator(prefix=b'block_'):
            height = key.decode('utf-8').split('_')[1]
            block_dict = utils.dump_pretty_dict(
                utils.load_dict(utils.bytes_to_str(value)))
            print(f'Height: {height}')
            print(block_dict)
            print()

    def print_meta(self):
        for key, value in self._db.iterator(prefix=b'meta_'):
            print(f'key: {key}, value: {value}')
    
    def _get_block(self, height, block_hash):
        block_key = self._get_block_key(height, block_hash)
        return utils.bytes_to_dict(self._get(block_key))

    def begin_transaction(self):
        self._write_batch = self._db.write_batch()

    def commit(self):
        self._write_batch.write()
        self._write_batch = None

    def _get(self, key):
        key_bytes = utils.to_bytes(key)
        value = self._db.get(key_bytes)
        if value == b'':
            return
        return value

    def _put(self, key, value):
        key = utils.to_bytes(key)
        value = utils.to_bytes(value)
        if self._db.get(key) != None \
        and key[:5] != b'meta_' \
        and key != b'height':
            raise PermissionError
        if self._write_batch:
            self._write_batch.put(key, value)
        else:
            self._db.put(key, value)

    def _increment_height(self):
        height = self.get_height()
        if height == None:
            height = 0
        else:
            height += 1
        self._put('height', height)
        return height

    def _prev_hash_is_correct(self, current_height, prev_hash):
        logging.info(f'current_height: {current_height}')
        logging.info(f'prev_hash: {prev_hash}')
        if self.get_height() == None:
            return True

        prev_height = self.get_block_height_by_hash(prev_hash)
        if prev_height != current_height - 1:
            return False

        block_dict = self.get_block_by_hash(prev_hash)
        if not block_dict:
            return False

        if block_dict['hash'] == prev_hash:
            return True

        return False

    def _signature_is_valid(self, block_dict):
        if not hasattr(self, 'signature_checker'):
            return True

        if not 'signature' in block_dict:
            return False
        return self.signature_checker(block_dict['signature'])