from pymemcache.client.hash import HashClient


class Client(HashClient):

    def disconnect_all(self):
        if not self.use_pooling:
            for client in self.clients.values():
                client.quit()

    def _get_client(self, key):
        client = HashClient._get_client(self, key)
        client.default_noreply = False
        return client
