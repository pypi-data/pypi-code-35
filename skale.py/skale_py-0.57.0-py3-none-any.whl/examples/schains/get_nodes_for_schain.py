from skale import Skale, BlockchainEnv
from skale.utils.helper import ip_from_bytes

skale = Skale(BlockchainEnv.AWS)

node_ids = skale.schains_data.get_node_ids_for_schain('CYBX9O59')
print(node_ids)

print('==========================')

nodes = skale.schains_data.get_nodes_for_schain('CYBX9O59')
print(nodes)

print('==========================')

nodes = skale.schains_data.get_nodes_for_schain_config('CYBX9O59')
print(nodes)