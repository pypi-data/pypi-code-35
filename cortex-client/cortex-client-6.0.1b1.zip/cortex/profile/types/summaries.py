"""
Copyright 2019 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from attr import attrs

from cortex.profile.utils.attr_utils import describableAttrib
from typing import Optional

__all__ = [
    'ProfileSummary'
]

@attrs(frozen=True)
class ProfileSummary(object):
    """
    Summary of a Profile ...
    """
    profileId = describableAttrib(type=str, description="What is the id for this profile?")
    profileSchema = describableAttrib(type=str, description="What is the id of the schema applied to this profile?")
    version = describableAttrib(type=int, description="How many modifications have been made to the profile?")
    updatedAt = describableAttrib(type=str, description="When was the most recent attribute appended to this profile?")
    createdAt = describableAttrib(type=Optional[str], default=None, description="When was the first attribute appended to this profile?")


# @attrs(frozen=True)
# class ProfileSchemaSummary(object):
#     """
#     Summary of a schema ...
#     """
#     schemaId = describableAttrib(type=str, description="What is the id of the schema?")
#     timestamp = describableAttrib(type=str, description="When was this schema created?")
#     profileType = describableAttrib(type=str, description="What type of profile is this schema for?")
#     attributes = describableAttrib(type=int, description="How many attributes are defined in the schema?")
#     tags = describableAttrib(type=int, description="How many tags are defined in the schema?")
#     groups = describableAttrib(type=int, description="How many groups are defined in the schema?")
#
#     # ----
#
#     @classmethod
#     def from_profile_schema(cls, schema: ProfileSchema) -> 'ProfileSchemaSummary':
#         return cls(
#             schemaId=schema.id,
#             timestamp=schema.createdAt,
#             profileType=schema.profileType,
#             attributes=None if schema.attributes is None else len(schema.attributes),
#             tags=None if schema.tags is None else len(schema.tags),
#             groups=None if schema.groups is None else len(schema.groups)
#         )
