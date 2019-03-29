from __future__ import division, absolute_import, print_function, unicode_literals

from mosaik.eid.eid_registry import EidRegistry
from mosaik.eid.eid_parser import EidParser
from mosaik.eid.entity_exception import EntityTypeException


class EntityIdentifier(str):
    def __new__(cls, e_type, e_index):
        """
        Generate an entity identifier from a given entity type and entity index.
        """
        if not EidRegistry.registered(e_type=e_type):
            raise EntityTypeException('Not a registered entity type:', e_type)

        e_type = EidParser.parse_entity_type(e_type)
        e_index = str(EidParser.parse_entity_index(e_index))
        entity_identifier = e_type.name + '-' + e_index

        return super(EntityIdentifier, cls).__new__(cls, entity_identifier)
