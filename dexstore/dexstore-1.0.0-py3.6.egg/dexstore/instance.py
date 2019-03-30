# -*- coding: utf-8 -*-
from graphenecommon.instance import AbstractBlockchainInstanceProvider, SharedInstance


class BlockchainInstance(AbstractBlockchainInstanceProvider):
    """ This is a class that allows compatibility with previous
        naming conventions
    """

    def __init__(self, *args, **kwargs):
        # Also allow 'dexstore_instance'
        if kwargs.get("dexstore_instance"):
            kwargs["blockchain_instance"] = kwargs["dexstore_instance"]
        AbstractBlockchainInstanceProvider.__init__(self, *args, **kwargs)

    def get_instance_class(self):
        """ Should return the Chain instance class, e.g. `dexstore.DexStore`
        """
        import dexstore as bts

        return bts.DexStore

    @property
    def dexstore(self):
        """ Alias for the specific blockchain
        """
        return self.blockchain


def shared_blockchain_instance():
    return BlockchainInstance().shared_blockchain_instance()


def set_shared_blockchain_instance(instance):
    instance.clear_cache()
    instance.set_shared_instance()


def set_shared_config(config):
    shared_blockchain_instance().set_shared_config(config)


shared_dexstore_instance = shared_blockchain_instance
set_shared_dexstore_instance = set_shared_blockchain_instance
