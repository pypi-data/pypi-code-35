import os
# 3rd Party 
from baybars.azure_table import AzureTable
from baybars.consul_values import ConsulValue
from baybars.kafka_consumer import KafkaListener
from baybars.timber import get_logger

logger = get_logger('BeastConsumer')

BATCH_SIZE = 100

KAFKA_HOST = 'profx/visual_search/kafka'
AZURE_STORAGE_ACCOUNT_NAME = 'profx/visual_search/account_name'
AZURE_STORAGE_ACCOUNT_KEY = 'profx/visual_search/account_key'

KAFKA_TOPIC_NAME = "beast-retailskus"



class BeastConsumer:
  def __init__(self):
    self.kafka_listener = KafkaListener('shared.kafka.eastus2.qa.jet.network:9092',
                                        'beast-retailskus',
                                        "beast-consumer-qa")
    self.consul = ConsulValue(os.environ.get("CONSUL_ADDR", "consul.qa.jet.com"))
    print(self.consul.get(KAFKA_HOST))
    print(self.consul.get(AZURE_STORAGE_ACCOUNT_KEY))
    print(self.consul.get(AZURE_STORAGE_ACCOUNT_NAME))
    self.table_client = AzureTable(self.consul.get(AZURE_STORAGE_ACCOUNT_NAME), 
                                 self.consul.get(AZURE_STORAGE_ACCOUNT_KEY), 
                                 "beast-retailskus"
                                 'id',
                                 'id')

  def process(self, batch):
    for item in batch:
      import ipdb; ipdb.set_trace()
      logger.info('batch={}'.format(item))

  def run(self):
    # TODO: Write to AzureTable
    while True:
      self.kafka_listener.consume(self.process, batch_size=BATCH_SIZE)


if __name__ == '__main__':
  BeastConsumer().run()