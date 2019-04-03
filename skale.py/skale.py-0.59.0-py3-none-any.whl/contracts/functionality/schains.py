from skale.contracts import BaseContract


class SChains(BaseContract):
    def get_schain_price(self, index_of_type, lifetime):
        return self.contract.functions.getSchainPrice(index_of_type,
                                                      lifetime).call()
