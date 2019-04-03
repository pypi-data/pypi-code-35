import requests


class AmoveoNode:
    def __init__(self, host):
        self.host = host

    def last_block(self):
        payload = ["height"]
        r = requests.get(self.host, json=payload)
        r.raise_for_status()
        data = r.json()
        return data[1]

    def block(self, block_num):
        # payload = ["block", block_num]
        payload = ["block", 3, block_num]
        r = requests.get(self.host, json=payload)
        r.raise_for_status()
        data = r.json()
        return data[1]

    def account(self, address: str):
        payload = ["account", address]
        r = requests.get(self.host, json=payload)
        r.raise_for_status()
        data = r.json()
        return data[1]

    def pending_tx(self):
        payload = ["mempool"]
        r = requests.get(self.host, json=payload)
        r.raise_for_status()
        data = r.json()
        return data[1]

    def prepare_tx(self, typ, amount, fee, _from, _to):
        payload = [typ, amount, fee, _from, _to]
        r = requests.get(self.host, json=payload)
        r.raise_for_status()
        data = r.json()
        return data[1]

    def send_tx(self, tx, sign):
        """
        :param tx:
        :param sign:
        :return:
        """
        payload = ["txs", [-6, ["signed", tx, sign, [-6]]]]
        r = requests.post(self.host, json=payload)
        r.raise_for_status()
        data = r.json()
        return data[1]
