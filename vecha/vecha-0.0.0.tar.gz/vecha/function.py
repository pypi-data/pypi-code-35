from functools import wraps
from vemodel import translator
from vemodel import Transaction, Clause


def encode_data(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        data = self.contract.encode_function(self.fn_name, *args)
        if not data:
            return None
        return func(self, data, **kwargs)
    return wrapper


class Function(object):

    def __init__(self, chain, contract, fn_name):
        super(Function, self).__init__()

        self.chain = chain
        self.contract = contract
        self.fn_name = fn_name

    @encode_data
    def __call__(self, data, pk, value):
        tx = Transaction(
            self.chain.chain_tag(),
            self.chain.current_block_ref(),
            Clause(self.contract.address, value, data)
        )
        send_data = {
            'raw': tx.sign(pk)
        }

        return self.contract.send(send_data)

    @encode_data
    def call(self, data, caller=None, value=0):
        call_data = {
            'caller': caller,
            'value': '%#x' % value,
            'data': data
        }

        result = self.contract.call(call_data)
        data = result.get('data', '')
        events = result.get('events', [])
        reverted = result.get('reverted', False)

        if reverted:
            result['data'] = translator.decode_revert_msg(data)
        else:
            result['data'] = self.contract.decode_result(self.fn_name, data)
            result['events'] = list(map(self.contract.decode_event, events))

        return result
