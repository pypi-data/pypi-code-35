from ktdk import log_config
import os

os.environ['KTDK_LOG_LEVEL'] = 'DEBUG'
os.environ['KTDK_DEVEL'] = 'True'

log_config.load_config(log_level_global='DEBUG')
