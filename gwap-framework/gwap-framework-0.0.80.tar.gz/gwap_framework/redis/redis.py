from redis import StrictRedis, ConnectionPool

from gwap_framework.singleton import Singleton


class RedisServer(StrictRedis, metaclass=Singleton):
    REDIS_HOST = None
    REDIS_PORT = None

    connection_poll = None
    redis = None

    def __init__(self) -> None:
        super(RedisServer, self).__init__(connection_pool=self.set_connection_pool())

    def set_connection_pool(self) -> 'ConnectionPool':
        return ConnectionPool(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=0,
        )
