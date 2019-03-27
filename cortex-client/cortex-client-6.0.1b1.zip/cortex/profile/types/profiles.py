from attr import attrs, validators

import cortex.profile.validators as custom_validators
from cortex.profile.constants.contexts import CONTEXTS
from cortex.profile.constants.types import VERSION, DESCRIPTIONS
from cortex.profile.types import ProfileAttribute, ProfileAttributeTypes
from cortex.profile.types.attributes import load_profile_attribute_from_dict
from cortex.profile.utils.attr_utils import describableAttrib, dicts_to_classes, attr_class_to_dict
from cortex.profile.utils import utc_timestamp

__all__ = [
    'Profile',
]

@attrs(frozen=True)
class Profile(object):
    """
    A representation of an entity's profile with pointers to specific attributes.
    """
    profileId = describableAttrib(type=str, description="What is the id of the profile?")
    profileSchema = describableAttrib(type=str, description="What schema was used to build this profile?")
    version = describableAttrib(
        type=int,
        validator=[validators.instance_of(int)],
        description="What version of attributes is this profile based off of?"
    )
    attributes = describableAttrib(
        type=ProfileAttribute,
        validator=[custom_validators.list_items_are_instances_of(ProfileAttributeTypes)],
        converter=lambda x: dicts_to_classes(x, ProfileAttribute, dict_constructor=load_profile_attribute_from_dict),
        description="What are all the historic version of this attribute?"
    )
    # With Defaults
    createdAt = describableAttrib(type=str, factory=utc_timestamp, description=DESCRIPTIONS.CREATED_AT)
    updatedAt = describableAttrib(type=str, factory=utc_timestamp, description=DESCRIPTIONS.UPDATED_AT)
    version = describableAttrib(type=str, default=VERSION, description="How many times has this profile been updated?")
    context = describableAttrib(type=str, default=CONTEXTS.PROFILE, description=DESCRIPTIONS.CONTEXT)

    def __iter__(self):
        return iter(attr_class_to_dict(self, hide_internal_attributes=True).items())