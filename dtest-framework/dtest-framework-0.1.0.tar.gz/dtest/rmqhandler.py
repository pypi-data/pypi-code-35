import pika


class RabbitMQHandler:
    def __init__(self, host, exchange, exchange_type):
        self.host = host
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.connect()

    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(
            exchange=self.exchange, exchange_type=self.exchange_type)

    def publishResults(self, jsonResults, exchange=None):
        if exchange is None:
            exchange = self.exchange
        self.channel.basic_publish(
            exchange=exchange, routing_key='', body=jsonResults)

    def closeConnection(self):
        self.connection.close()
