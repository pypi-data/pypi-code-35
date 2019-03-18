"""
Amatino API
Tree Module
Author: hugh@amatino.io
"""
from typing import Type
from typing import TypeVar
from typing import List
from typing import Optional
from typing import Any
from typing import Dict
from datetime import datetime
from amatino.denominated import Denominated
from amatino.denomination import Denomination
from amatino.decodable import Decodable
from amatino.internal.data_package import DataPackage
from amatino.internal.api_request import ApiRequest
from amatino.internal.url_parameters import UrlParameters
from amatino.internal.http_method import HTTPMethod
from amatino.internal.encodable import Encodable
from amatino.missing_key import MissingKey
from amatino.entity import Entity
from amatino.unexpected_response_type import UnexpectedResponseType
from amatino.internal.am_time import AmatinoTime
from amatino.tree_node import TreeNode
from amatino.internal.immutable import Immutable
from amatino.global_unit import GlobalUnit
from amatino.custom_unit import CustomUnit

T = TypeVar('T', bound='Tree')


class Tree(Decodable, Denominated):
    """
    Trees present the entire chart of Accounts of an Entity in a single
    hierarchical object.

    Each Account is nested under its parent, and in turn lists all its
    children, all providing Balances and Recursive Balances.

    Trees are trimmed for permissions. If the user requesting the tree only
    has read access to a subset of Accounts, they will only receive a tree
    containing those accounts, with placeholder objects filling the place
    of Accounts they are not permitted to read.

    Each Account in the Tree is presented as a Tree Node.
    """
    _PATH = '/trees'

    def __init__(
        self,
        entity: Entity,
        balance_time: AmatinoTime,
        generated_time: AmatinoTime,
        global_unit_denomination: Optional[int],
        custom_unit_denomination: Optional[int],
        tree: Optional[List[TreeNode]]
    ) -> None:

        assert isinstance(entity, Entity)
        assert isinstance(balance_time, AmatinoTime)
        assert isinstance(generated_time, AmatinoTime)
        if global_unit_denomination is not None:
            assert isinstance(global_unit_denomination, int)
        if custom_unit_denomination is not None:
            assert isinstance(custom_unit_denomination, int)
        if tree is not None:
            assert isinstance(tree, list)
            assert False not in [isinstance(t, TreeNode) for t in tree]
        
        self._entity = entity
        self._balance_time = balance_time
        self._generated_time = generated_time
        self._global_unit_id = global_unit_denomination
        self._custom_unit_id = custom_unit_denomination
        self._tree = tree

        return

    entity = Immutable(lambda s: s._entity)
    session = Immutable(lambda s: s._entity.session)
    start_time = Immutable(lambda s: s._start_time)
    end_time = Immutable(lambda s: s._end_time)
    generated_time = Immutable(lambda s: s._generated_time)
    custom_unit_id = Immutable(lambda s: s._custom_unit_id)
    global_unit_id = Immutable(lambda s: s._global_unit_id)
    nodes = Immutable(lambda s: s._tree)

    has_accounts = Immutable(
        lambda s: s._nodes is not None and len(s._nodes) > 0
    )

    @classmethod
    def decode(cls: Type[T], entity: Entity, data: Any) -> T:

        if not isinstance(data, dict):
            raise UnexpectedResponseType(data, dict)

        try:
            tree = None
            if data['tree']