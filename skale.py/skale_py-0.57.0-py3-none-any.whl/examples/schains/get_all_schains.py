from skale import Skale, BlockchainEnv

skale = Skale(BlockchainEnv.DO)
schains = skale.schains_data.get_all_schains()

print(schains)