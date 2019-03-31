import pika


class MQChecker:
    def __init__(self, host, port, user, password):
        self.credentials = pika.credentials.PlainCredentials(user, password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=host, port=port,
                credentials=pika.credentials.PlainCredentials(user, password)
            )
        )
        self.channel = self.connection.channel()

    def queue_declare(self, queue):
        return self.channel.queue_declare(queue=queue, passive=True)

    def close(self):
        if self.connection:
            self.connection.close()

    def get_message_count(self, queue):
        return self.queue_declare(queue).method.message_count

    def get_consumer_count(self, queue):
        return self.queue_declare(queue).method.message_count
