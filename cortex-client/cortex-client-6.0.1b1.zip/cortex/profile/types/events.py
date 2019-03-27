from typing import Optional

from attr import attrs

from cortex.profile.utils.attr_utils import describableAttrib, dict_to_attr_class, attr_class_to_dict, time_converter


__all__ = [
    'EventSource',
    'EntityEvent',
]

@attrs(frozen=True)
class EventSource(object):
    title = describableAttrib(type=str)
    description = describableAttrib(type=Optional[str])
    rights = describableAttrib(type=Optional[str])
    category = describableAttrib(type=Optional[str])
    sector = describableAttrib(type=Optional[str])
    region = describableAttrib(type=Optional[str])
    creator = describableAttrib(type=Optional[str])
    publisher = describableAttrib(type=Optional[str])
    language = describableAttrib(type=Optional[str])
    url = describableAttrib(type=Optional[str])


@attrs(frozen=True)
class EntityEvent(object):
    """
    Representation of all the Historic Values Associated with a Profile Attribute
    """
    event = describableAttrib(type=str, description="What is the name of the event?")
    entityType = describableAttrib(type=str, description="What is the type of the entity?")
    entityId = describableAttrib(type=str, description="Does this event relate an entity to another entity?")
    properties = describableAttrib(type=dict, factory=dict, description="What are the properties associated with this event?")
    meta = describableAttrib(type=dict, factory=dict, description="What is custom metadata associated with this event?")
    # With Defaults ...
    targetEntityId = describableAttrib(type=Optional[str], default=None, description="Does this event relate an entity to another entity?")
    targetEntityType = describableAttrib(type=Optional[str], default=None, description="What is the type of entity this event relates to?")
    eventLabel = describableAttrib(type=Optional[str], default=None, description="What is the name of the event?")
    eventTime = describableAttrib(
        type=Optional[int],
        default=None,  # The timestamp used in node is 1k times the arrow timestamp.
        converter=time_converter,
        description="When did the event occur?"
    )
    source = describableAttrib(
        type=Optional[EventSource],
        default=None,  # The timestamp used in node is 1k times the arrow timestamp.
        converter=lambda x: dict_to_attr_class(x, EventSource),
        description="What is the name of the event?"
    )

    def __iter__(self):
        # Skipping nulls ... so that the JS defaults kick into place ...
        return iter(attr_class_to_dict(self, hide_internal_attributes=True, skip_nulls=True).items())