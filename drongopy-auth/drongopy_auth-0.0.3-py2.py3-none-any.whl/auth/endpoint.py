from drongo.utils.endpoint import APIEndpoint


class AuthAPIEndpoint(APIEndpoint):
    __auth_permissions__ = []

    def check_permissions(self):
        pass
