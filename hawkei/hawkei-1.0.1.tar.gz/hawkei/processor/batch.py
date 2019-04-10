import logging
import json

MAX_BYTES = 204800 # 200Kb
MAX_MESSAGES = 100
MAX_MESSAGE_BYTES = 32768 # 32Kb

class Batch():
    logger = logging.getLogger('hawkei')

    def __init__(self):
        self.total_bytes = 0
        self.messages = []

    def add(self, message):
        message_size = len(json.dumps(message).encode())

        if self.is_max_message_reached(message_size):
            self.logger.error('message is too large to be sent')
            return False

        self.total_bytes += message_size
        self.messages.append(message)
        return True


    def is_empty(self):
        return len(self.messages) == 0

    def is_full(self):
        return self.is_max_messages_reached() or self.is_max_size_reached()

    def is_max_messages_reached(self):
        return len(self.messages) >= MAX_MESSAGES

    def is_max_size_reached(self):
        return self.total_bytes >= MAX_BYTES

    @classmethod
    def is_max_message_reached(cls, message_json_size):
        return message_json_size > MAX_MESSAGE_BYTES
