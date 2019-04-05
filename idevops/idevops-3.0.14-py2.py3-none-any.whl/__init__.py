VERSION='3.0.14'

# default variables
CONF_DIR = '.idevops'
SEED_NAME = 'node-0'
ISERVER_KEYPAIR_GENERATOR = 'gen_keypair.go'
ISERVER_KEYPAIR_OF_MASTER = 'keypairs_master'
ISERVER_KEYPAIR_OF_SLAVE = 'keypairs_slave'
ISERVER_GENESIS = 'genesis.yml'
SHEADER = [u'name', u'type', u'region', u'instance_type', u'image']
DHEADER = [u'eip']
AWS_EBS_ROOT_DEFAULT_SIZE = 50
AWS_EBS_DATA_DEFAULT_SIZE = 500
AWS_EBS_DATA_MOUNT_POINT = '/dev/xvdb'
AWS_EBS_DATA_TYPE = 'st1'
