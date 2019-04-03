from translator import *


class FunctionCoder(object):

    def __init__(self, *fn_abi_list):
        super(FunctionCoder, self).__init__()

        self.function_data = {}

        for abi in fn_abi_list:
            if abi.get('type', None) != 'function':
                continue

            if 'signature' not in abi:
                continue

            normalized_name = normalize_name(abi['name'])
            encode_types = [
                element['type']
                for element in abi.get('inputs', [])
            ]
            decode_types = [
                element['type']
                for element in abi.get('outputs', [])
            ]
            self.function_data[normalized_name] = {
                'prefix': int(abi.get('signature', '0x0'), 16),
                'encode_types': encode_types,
                'decode_types': decode_types,
                'is_call': abi.get('constant', False)
            }

    def is_call(self, function_name):
        if function_name not in self.function_data:
            print(ValueError('Unkown function {}'.format(function_name)))
            return False

        function = self.function_data[function_name]
        return function['is_call']

    def encode_function(self, function_name, *args):
        """ Return the encoded function call.

        Args:
            function_name (str): One of the existing functions described in the
                contract interface.
            args (List[Any]): The function arguments that wll be encoded and
                used in the contract execution in the vm.

        Return:
            bin: The encoded function name and arguments so that it can be used
                 with the evm to execute a funcion call, the binary string follows
                 the Ethereum Contract ABI.
        """

        if function_name not in self.function_data:
            print(ValueError('Unkown function {}'.format(function_name)))
            return None

        function = self.function_data[function_name]

        function_selector = zpad(encode_int(function['prefix']), 4)
        arguments = encode_abi(function['encode_types'], args)

        return '0x' + encode_hex(function_selector + arguments)

    def decode_result(self, function_name, data):
        """ Return the function call result decoded.

        Args:
            function_name (str): One of the existing functions described in the
                contract interface.
            data (str): The encoded result from calling `function_name`.

        Return:
            List[any]: The values returned by the call to `function_name`.
        """
        function = self.function_data[function_name]
        arguments = decode_abi(function['decode_types'], decode_hex(data))
        return arguments


if __name__ == "__main__":
    abi = {
        "constant": False,
        "inputs": [
          {
              "name": "_id",
              "type": "uint256"
          }
        ],
        "name": "finish",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function",
        "signature": "0xd353a1cb"
    }
    fc = FunctionCoder(abi)
    # fc.encode_function(abi['name'], 1)
    # print(r == '0xd353a1cb0000000000000000000000000000000000000000000000000000000000000001')
    r = fc.decode_revert_msg('0x08c379a00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000000f5175697a206e6f74206578697465640000000000000000000000000000000000')
    print(r)
