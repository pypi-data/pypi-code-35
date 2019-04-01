class AuthStartResult(object):

    def __init__(self, model):
        self.__nonce = model.get('toSignData', None)
        self.__digest_algorithm = model.get('digestAlgorithmName', None)
        self.__digest_algorithm_oid = model.get('digestAlgorithmOid', None)

    @property
    def nonce(self):
        return self.__nonce

    @nonce.setter
    def nonce(self, value):
        self.__nonce = value

    @property
    def digest_algorithm(self):
        return self.__digest_algorithm

    @digest_algorithm.setter
    def digest_algorithm(self, value):
        self.__digest_algorithm = value

    @property
    def digest_algorithm_oid(self):
        return self.__digest_algorithm_oid

    @digest_algorithm_oid.setter
    def digest_algorithm_oid(self, value):
        self.__digest_algorithm_oid = value


__all__ = ['AuthStartResult']
