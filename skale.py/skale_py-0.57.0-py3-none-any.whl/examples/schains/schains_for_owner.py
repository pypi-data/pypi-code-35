import sys
from skale import Skale, BlockchainEnv
skale = Skale(BlockchainEnv.AWS)

account = sys.argv[1]

res = skale.schains_data.get_schains_for_owner(account)
print(res)