import os
import scipy

from Kraken import time, KrakenController, getBasicController, BLOCK_SIZE

blob = getBasicController()

kin = input('\nKill all idle tentacles? (y/n):\n')
if kin in ['y', 'yes']:
    blob.killTentacles()
