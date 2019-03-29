from request import Request, get


class Chain(object):

    def __init__(self, endpoint: str):
        self.blocks = Request(endpoint).blocks
        super(Chain, self).__init__()

    def best_blcok_num(self):
        blk = self.blocks('best').make_request(get)
        return blk['number']

    def current_block_ref(self):
        blk = self.blocks('best').make_request(get)
        return int(blk['id'].encode("utf-8")[2:10], 16)

    def chain_tag(self):
        blk = self.blocks(0).make_request(get)
        return int(blk['id'][-2:], 16)


if __name__ == "__main__":
    c = Chain('https://sync-testnet.vechain.org')
    print(c.current_block_ref())
