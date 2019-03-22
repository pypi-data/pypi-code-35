# -*- coding: utf-8 -*-

from facture.registry import RouteRegistry
from facture.core.component import BaseComponent


class BaseController(BaseComponent):
    """Controller base class"""

    @classmethod
    def register(cls, pkg):
        """Makes the package available to this controller.

        :param pkg: facture.Jetpack
        """

        cls._pkg_bind(pkg)

    async def on_ready(self):
        """Called upon initialization"""

    async def on_request(self, *args):
        """Called upon request arrival"""

    @property
    def stacks(self):
        """Route registry iterator

        Iterates over RouteStacks, takes the stack.name (which corresponds to the handler function name)
        and returns reference to its instance method, along with the stack itself (schemas, paths, methods etc).

        :return: (<handler name>, <stack>)
        """

        for stack in RouteRegistry.stacks.values():
            # Yield only if the stack belongs to the Controller being iterated on
            if stack.handler.__module__ == self.__module__:
                yield getattr(self, stack.name), stack

    def __repr__(self):
        return f'<{self.__class__.__name__} at {hex(id(self))}>'
