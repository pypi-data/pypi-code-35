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
from typing import List

import deprecation
import attr
from cortex.logger import getLogger
from cortex.profile import Profile, ProfileSchema
from cortex.profile.types import EntityEvent, ProfileAttributeType, ProfileSchema as ProfileSchemaType, ProfileAttributeSchema, \
    ProfileTagSchema, ProfileFacetSchema, ProfileTaxonomySchema
from cortex_client import ProfilesClient

log = getLogger(__name__)

__all__ = [
    "ProfileBuilder",
    "ProfileSchemaBuilder",
]


class ProfileBuilder:

    """
    A builder utility to aid in programmatic creation of Cortex Profiles.  Not meant to be directly instantiated by
    clients.
    """

    def __init__(self, profileId:str, schemaId:str, client: ProfilesClient):
        self._profileId = profileId
        self._schemaId = schemaId
        self._profiles_client = client
        self._events = []

    def with_events(self, events:List[EntityEvent]):
        """
        Appends the provided events to the list of events that will be used to build profiles.
        :param events:
        :return:
        """
        self._events.extend(events)
        return self

    @deprecation.deprecated(deprecated_in='6.0.1b1', details='Use with_events instead.')
    def with_attributes(self, attributes:List[ProfileAttributeType]):
        """
        Converts the provided attributes into a list of events and appends them to the list of events that will be
        used to build profiles.
        :param events:
        :return:
        """
        self._events.extend([
            self._profiles_client._turn_attribute_into_entity_event(a) for a in attributes
        ])
        return self

    def build(self) -> Profile:
        """
        Pushes profile building events then retrieves the latest profile ...

        :return: the resulting Connection
        """
        # Todo: You can push events for any profile ... not just the profileId specified when instantiating the builder.
        # Push events
        self._profiles_client.pushEvents(self._events)
        # Retrieve the specified profiles ...
        return Profile.get_profile(self._profileId, self._schemaId, self._profiles_client)


class ProfileSchemaBuilder:

    """
    A builder utility to aid in programmatic creation of Cortex Profiles.  Not meant to be directly instantiated by
    clients.
    """

    def __init__(self, schemaName:ProfileSchemaType, client: ProfilesClient):
        self._schema = ProfileSchemaType(
            name=schemaName,
            title=schemaName,
            profileType=schemaName,
            description=schemaName,
        )
        self._profiles_client = client

    def name(self, name:str) -> 'ProfileSchemaBuilder':
        """
        Sets the name of the schema ...
        :param name:
        :return:
        """
        self._schema = attr.evolve(self._schema, name=name)
        return self

    def title(self, title:str) -> 'ProfileSchemaBuilder':
        """
        Sets the title of the schema ...
        :param title:
        :return:
        """
        self._schema = attr.evolve(self._schema, title=title)
        return self

    def profileType(self, profileType:str) -> 'ProfileSchemaBuilder':
        """
        Sets the profileType of the schema ...
        :param profileType:
        :return:
        """
        self._schema = attr.evolve(self._schema, profileType=profileType)
        return self

    def description(self, description:str) -> 'ProfileSchemaBuilder':
        """
        Sets the description of the schema ...
        :param description:
        :return:
        """
        self._schema = attr.evolve(self._schema, description=description)
        return self

    def facets(self, facets:List[ProfileFacetSchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the facets of the schema ...
        :param facets:
        :return:
        """
        self._schema = attr.evolve(self._schema, facets=facets)
        return self

    def taxonomy(self, taxonomy:List[ProfileTaxonomySchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the taxonomy of the schema ...
        :param taxonomy:
        :return:
        """
        self._schema = attr.evolve(self._schema, taxonomy=taxonomy)
        return self

    def attributes(self, attributes:List[ProfileAttributeSchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the attributes of the schema ...
        :param attributes:
        :return:
        """
        self._schema = attr.evolve(self._schema, attributes=attributes)
        return self

    def attributeTags(self, attributeTags:List[ProfileTagSchema]) -> 'ProfileSchemaBuilder':
        """
        Sets the attributeTags of the schema ...
        :param attributeTags:
        :return:
        """
        self._schema = attr.evolve(self._schema, attributeTags=attributeTags)
        return self

    def build(self) -> ProfileSchema:
        """
        Builds and saves a new Profile Schema using the properties configured on the builder
        :return:
        """
        # Push Schema ...
        self._profiles_client.pushSchema(self._schema)
        # Get latest scheam ...
        return ProfileSchema.get_schema(self._schema.name, self._profiles_client)
