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

from cortex.profile.types import ProfileVersionSummary, HistoricProfile, Profile as ProfileType, \
    ProfileSchema as ProfileSchemaType

from ..camel import Document, CamelResource
from ..logger import getLogger

log = getLogger(__name__)

__all__ = [
    'Profile',
    'ProfileSchema'
]

class Profile(Document):
    """
    Accessing an existent Cortex Profile.
    """

    @staticmethod
    def get_profile(profileId:str, schema_id:str, profile_client) -> 'Profile':
        """
        Fetches a profile adhering to a specific schema ...
        """
        profile = profile_client.describeProfile(profileId, schema_id)
        return Profile(profile if profile else {}, profile_client)

    def __init__(self, profile:ProfileType, profile_client):
        super().__init__(dict(profile), True)
        self._profile = profile
        self._profile_client = profile_client

    def latest(self) -> ProfileType:
        return self._profile

    def historic(self) -> HistoricProfile:
        """
        Gets the historic version of the profile
        :return:
        """
        return self._profile_client.describeHistoricProfile(self.profileId, self.profileSchema)

    def delete(self) -> bool:
        """
        Deletes the profile ...
        :return:
        """
        return self._profile_client.deleteProfile(self.profileId, self.profileSchema)

    def versions(self) -> List[ProfileVersionSummary]:
        """
        Lists the different versions of the profile ...
        :return:
        """
        return self._profile_client.listVersions(self.profileId, self.profileSchema)

    def __repr__(self):
        return self._profile.__repr__()


class ProfileSchema(CamelResource):
    """
    Accessing an existent Cortex ProfileSchema.
    """

    @staticmethod
    def get_schema(schema_id:str, profile_client) -> 'ProfileSchema':
        """
        Fetches the requested schema by id ...
        """
        schema = profile_client.describeSchema(schema_id)
        return ProfileSchema(schema if schema else {}, profile_client)

    def __init__(self, profile_schema:ProfileSchemaType, profile_client):
        super().__init__(profile_schema.to_dict_with_internals(), True)
        self._schema = profile_schema
        self._profile_client = profile_client

    def delete(self) -> bool:
        """
        Deletes the schema ...
        :return:
        """
        return self._profile_client.deleteSchema(self.schemaId)

    def __repr__(self):
        return repr(self._schema)