from request import post
from functools import wraps
from vemodel import translator
from vemodel import Transaction, Clause


def _encode_data(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        data = self.fn_coder.encode_function(self.fn_name, *args)
        if not data:
            return None
        return func(self, data, **kwargs)
    return wrapper


class Function(object):

    def __init__(self, chain, contract, request, fn_coder, event_decoder, fn_name):
        super(Function, self).__init__()

        self.chain = chain
        self.contract = contract
        self.request = request
        self.fn_coder = fn_coder
        self.event_decoder = event_decoder
        self.fn_name = fn_name

    @_encode_data
    def __call__(self, data, pk, value):
        tx = Transaction(
            self.chain.chain_tag(),
            self.chain.current_block_ref(),
            Clause(self.contract, value, data)
        )
        send_data = {
            'raw': tx.sign(pk)
        }

        r = self.request.transactions.make_request(post, data=send_data)
        return r.get('id', None)

    @_encode_data
    def call(self, data, caller=None, value=0):
        call_data = {
            'caller': caller,
            'value': '%#x' % value,
            'data': data
        }

        result = self.request.accounts(self.contract).make_request(post, data=call_data)
        data = result.get('data', '')
        events = result.get('events', [])
        reverted = result.get('reverted', False)

        if reverted:
            result['data'] = translator.decode_revert_msg(data)
        else:
            result['data'] = self.fn_coder.decode_result(self.fn_name, data)
            result['events'] = list(map(self.event_decoder.decode_event, events))
        return result
