import os
from skale.utils.helper import private_key_to_public, public_key_to_address

pr =  os.environ['ETH_PRIVATE_KEY']
pk = private_key_to_public(pr)
print(pk)

address = public_key_to_address(pk)
print(address)
