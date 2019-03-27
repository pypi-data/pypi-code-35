from skale import Skale, BlockchainEnv
skale = Skale(BlockchainEnv.AWS)


res = skale.schains_data.get_schains_for_node(0)
print(res)