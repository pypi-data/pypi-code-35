# -*- coding: utf-8 -*-
from pyramid.security import Allow, Authenticated

DEFAULT_PERM = [(Allow, Authenticated, "oauth"), ]


class RootFactory(dict):
    """
       Ressource factory, returns the appropriate resource regarding
       the request object
    """
    __name__ = "root"

    def __init__(self, request):
        self.request = request

    @property
    def __acl__(self):
        """
            Default permissions
        """
        acl = DEFAULT_PERM[:]
        return acl
