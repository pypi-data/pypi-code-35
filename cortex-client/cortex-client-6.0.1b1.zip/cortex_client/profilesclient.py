
"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

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
import base64
import traceback
import urllib
from typing import List, Optional

import arrow
import deprecation
import pydash
from requests.exceptions import HTTPError

from cortex.profile.types import MessageResponse, Profile, ProfileSchema, EntityEvent, ProfileSummary, \
    DeclaredProfileAttribute, ProfileAttribute, EntityAttributeValue
from cortex.profile.utils import head, dicts_to_classes, dict_to_attr_class, construct_attr_class_from_dict, utc_timestamp
from cortex_client.authenticationclient import AuthenticationClient
from cortex_client.client import _Client
from cortex_client.secretsclient import SecretsClient

OrderedList = List
NoneType = type(None)


class ProfilesClient(_Client):
    """A client for the Cortex Profiles SDK Functionality."""

    URIs = {
        'events': 'graph/events/entities',
        'profiles': 'graph/profiles',
        'schemas': 'graph/profiles/schemas',
        'schema':  'graph/profiles/schemas/{schemaId}',
        'profile': 'graph/profiles/{profileId}',
    }

    def __init__(self, url, version, token, beta_mode=True):
        super(ProfilesClient, self).__init__(url, version, token)
        if beta_mode:
            # Download the cortex next secret ...
            next = self._load_cortex_next_params()
            # Get a jwt using the secret ...
            ac = AuthenticationClient(next["url"], 2)
            next_token = next.get("token") or ac.fetch_auth_token(next["account"], next["username"], next["password"])
            # Init client to point to endpoint specified in the cortex next secret ...
            super(ProfilesClient, self).__init__(next["url"], version, next_token)

    def _load_cortex_next_params(self) -> str:
        """
        Temporary placeholder to load a secret that points to the cortex next stack ...
        When the graph service is available in prod, this will no longer be relevant ...
        :return:
        """
        secretsclient = SecretsClient(self._serviceconnector.url, "2", self._serviceconnector.token)
        secret = secretsclient.get_secret("cortex-next")
        if not secret:
            raise Exception("Failed to get secret.")
        secret = pydash.merge(secret, {"password": base64.b64decode(secret["password"].encode("utf-8")).decode("utf-8").strip('\n')})
        return secret

    def findProfiles(self, query:Optional[dict]={}) -> List[ProfileSummary]:
        """
        Finding profiles in the system.

        :param query: An optional mongo-oritented query that can reduce the amount of profiles found.
        :return:
        """
        profiles = self._get_json(self.URIs["profiles"])["profiles"]
        return dicts_to_classes(profiles, ProfileSummary)

    def listSchemas(self) -> List[ProfileSchema]:
        """
        List all of the schemas currently loaded into the system.
        :return:
        """
        schemas = self._get_json(self.URIs["schemas"])["schemas"]
        return dicts_to_classes(schemas, ProfileSchema)

    def pushSchema(self, schema:ProfileSchema) -> MessageResponse:
        return MessageResponse(**self._post_json(self.URIs["schemas"], dict(schema)))

    def describeSchema(self, schemaId:str, version:Optional[str]=None) -> Optional[ProfileSchema]:
        """
        >>> describeSchema("cortex/end-user")
        :param schemaId: The name of the schema we are interested in describinb.
        :param version: By default, the latest version of the schema is returned, otherwise, the version indicated.
        :return: The profile schema if found, otherwise None.
        """
        try:
            schema = self._get_json(self.URIs["schema"].format(schemaId=schemaId))
        except Exception as e:
            print(e)
            schema = None
        return dict_to_attr_class(schema, ProfileSchema)

    def deleteSchema(self, schemaId:str) -> bool:
        """
        Deletes a schema ...
        :param schemaId:
        :return: True if the schema is successfully deleted, false otherwise ...
        """
        try:
            r = self._serviceconnector.request('DELETE', self.URIs["schema"].format(schemaId=schemaId))
            r.raise_for_status()
        except HTTPError as e:
            print(e)
            return False
        return True

    def describeProfile(
            self, profileId:str, schemaId:str,
            historic:Optional[bool]=None, version:Optional[str]=None) -> Optional[Profile]:
        """
        Get the profile at a specific version ...
        If no version is specified, the latest profile is returned ...

        :param profileId:
        :param schemaIds: What schemas do we want to get the profile for ...?
        :param version: What version do we want to limit the profile to?
        :return:
        """
        if schemaId is None:
            raise Exception("schemaId required.")
        try:
            url = self.URIs["profile"].format(profileId=profileId)
            url = url if schemaId is None else "{}?{}".format(url, urllib.parse.urlencode({"schemaNames": schemaId}))
            raw_profiles = self._get_json(url)
            profile = head([
                profile for profile in raw_profiles.get("profiles", []) if profile["profileSchema"] == schemaId
            ])
            p = dict_to_attr_class(profile, Profile)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            p = None
        return p

    # Profile Ops ...
    def deleteProfile(self, profileId: str, schemaId:Optional[str]=None) -> bool:
        try:
            url = self.URIs["profile"].format(profileId=profileId)
            url = url if schemaId is None else "{}?{}".format(url, urllib.parse.urlencode({"schema": schemaId}))
            r = self._serviceconnector.request('DELETE', url)
            r.raise_for_status()
        except HTTPError as e:
            print(e)
            return False
        return True

    def pushEvents(self, events:List[EntityEvent]) -> Optional[List[str]]:
        response = self._post_json(self.URIs["events"], [
            dict(e) for e in events
        ])
        return [
            r.get("message") for r in response
        ]

    @deprecation.deprecated(deprecated_in='6.0.1b1', details='Use pushEvents instead.')
    def pushAttributes(self, profileId:str, attributes:List[ProfileAttribute]) -> List[str]:
        """
        Pushes attributes to the latest profile for the specified profileId.
        Returns a list of messages with regards to the status of each attribute being pushed ...

        :param profileId:
        :param attributes:
        :return:
        """
        return self.pushEvents([
            self._turn_attribute_into_entity_event(a) for a in attributes
        ])

    def _turn_attribute_into_entity_event(self, attribute:ProfileAttribute) -> EntityEvent:
        """
        Transforms an attribute into an entity event.
            If type(attribute) == ProfileAttribute[EntityAttributeValue] then the Entity Event captured
                within the attribute is used as is ...
            Otherwise ... the attribute is converted into an entity event where ...
                - The attributeKey is used as the event
                - The time of the attributeCreation is used as the eventTime ...
                - The attributeValue is used as the properties as is ...
        :param attribute:
        :return:
        """
        if isinstance(attribute.attributeValue, EntityAttributeValue):
            return attribute.attributeValue
        else:
            return EntityEvent(
                event=attribute.attributeKey,
                entityId=attribute.profileId,
                entityType=attribute.profileSchema,
                eventTime=attribute.createdAt,
                properties=dict(attribute.attributeValue)
            )

    def _turn_entity_event_into_attribute(
            self, entityEvent:EntityEvent, attributeType:type=DeclaredProfileAttribute, attributeValueType:type=EntityAttributeValue) -> ProfileAttribute:
        """
        Transforms an attribute into an entity event.
            If type(attribute) == ProfileAttribute[EntityAttributeValue] then the Entity Event captured
                within the attribute is used as is ...
            Otherwise ... the attribute is converted into an entity event where ...
                - The attributeKey is used as the event
                - The time of the attributeCreation is used as the eventTime ...
                - The attributeValue is used as the properties as is ...
        :param attribute:
        :return:
        """
        if attributeValueType == EntityAttributeValue:
            return attributeType(
                profileId=entityEvent.entityId,
                profileSchema=entityEvent.entityType,
                attributeKey=entityEvent.event,
                attributeValue=entityEvent,
                createdAt=arrow.get(entityEvent.eventTime/1000),
            )
        else:
            return attributeType(
                profileId=entityEvent.entityId,
                profileSchema=entityEvent.entityType,
                attributeKey=entityEvent.event,
                attributeValue=construct_attr_class_from_dict(attributeValueType, entityEvent.properties),
                createdAt=arrow.get(entityEvent.eventTime/1000) if entityEvent.eventTime is not None else utc_timestamp(),
            )

    # PHASE 2

    # def describeAttributeByKey(self, profileId: str, attributeKey: str, commitId: Optional[str] = None) -> Optional[
    #     ProfileAttribute]:
    #     """
    #     Describe a specific attribute in the profile ...
    #     Either attributeId or attributeKey must be provided ... attributeId takes precedence over attributeKey ...
    #     If attribute key is provided ... the
    #     :param profileId:
    #     :param attributeKey:
    #     :param commitId:
    #     :return:
    #     """
    #     commit = (
    #         self._internal_profiles_client.get_latest_profile_commit(profileId)
    #         if commitId is None else self._internal_profiles_client.get_commit_by_id(commitId)
    #     )
    #     if not commit:
    #         return None
    #     return self._internal_profiles_client.get_attribute_by_key(profileId, attributeKey, commit.id)
    #
    # def listCommits(self, profileId: str) -> List[ProfileCommitSummary]:
    #     """
    #     Lists all of the modifications done on the profile ... with the date of each modification!
    #
    #     :param profileId:
    #     :return:
    #     """
    #     return [
    #         ProfileCommitSummary.from_profile_commit(commit)
    #         for commit in self._internal_profiles_client.get_commit_history_for_profile(profileId)
    #     ]
    #
    # def listAttributes(self, profileId: str) -> Optional[List[ProfileAttributeSummary]]:
    #     """
    #     List all of the attributes currently in the profile adhering to a specific schema.
    #     Get the profile as of a certain commit
    #         ... defaults to latest commit if no commitId is specified ...
    #     :param profileId:
    #     :param commitId:
    #     :return:
    #     """
    #     profile = self.describeProfile(profileId, commitId)
    #     attributes = profile.attributes if profile is not None else []
    #     return list(map(ProfileAttributeSummary.from_profile_attribute, attributes))
    #
    # def describeCommit(self, commitId:str):
    #     """
    #     Describe a specific commit ...
    #     :param commitId:
    #     :return:
    #     """
    #     return self._internal_profiles_client.get_commit_by_id(commitId)
    #
    #
    # def describeAttributeById(self, attributeId:str) -> Optional[ProfileAttribute]:
    #     """
    #     Describe a specific attribute in the profile ...
    #     Either attributeId or attributeKey must be provided ... attributeId takes precedence over attributeKey ...
    #     If attribute key is provided ... the
    #     :param attributeId:
    #     :return:
    #     """
    #     return self._internal_profiles_client.get_attribute_by_id(attributeId)

    # PHASE 3

    # def findProfilesWithAttributes(self, list_of_attribute_keys:List[str], all:bool=False, none:bool=False, any:bool=False) -> List[str]:
    #     """
    #     Finds all profile with the attributes specified.
    #
    #     :param list_of_attribute_keys: List of attribute keys profiles must contain ...
    #     :return:
    #     """
    #     if all:
    #         return self._internal_profiles_client.find_profiles_with_all_attributes(list_of_attribute_keys)
    #     if none:
    #         return self._internal_profiles_client.find_profiles_with_none_of_the_attributes(list_of_attribute_keys)
    #     if any:
    #         return self._internal_profiles_client.find_profiles_with_any_of_the_attributes(list_of_attribute_keys)
    #     return []
    #
    # def findProfilesUpdatedBetween(self, start_time:str, end_time:str):
    #     return self._internal_profiles_client.find_profiles_updated_between(start_time, end_time)
    #
    # def findBottomProfilesForAttributeWithCounterValue(self, attributeKey: str, n=5):
    #     return pd.DataFrame([
    #         {
    #             "profileId": attribute["profileId"],
    #             "attributeKey": attribute["attributeKey"],
    #             "attributeValue": attribute["attributeValue"]["value"]
    #         }
    #         for attribute in self._internal_profiles_client.sort_counter_based_attributes(attributeKey, pick=n, ascending=True)
    #     ], columns=["profileId", "attributeKey", "attributeValue"])
    #
    # def findTopProfilesForAttributeWithCounterValue(self, attributeKey:str, n=5):
    #     return pd.DataFrame([
    #         {
    #             "profileId": attribute["profileId"],
    #             "attributeKey": attribute["attributeKey"],
    #             "attributeValue": attribute["attributeValue"]["value"]
    #         }
    #         for attribute in
    #         self._internal_profiles_client.sort_counter_based_attributes(attributeKey, pick=n, ascending=False)
    #     ], columns=["profileId", "attributeKey", "attributeValue"])
    #
    # def countsOfLatestAttributesPerProfile(self, query:Optional[dict]=None) -> pd.DataFrame:
    #     return pd.DataFrame(
    #         self._internal_profiles_client.counts_of_latest_attributes_per_profile(query),
    #         columns=["profileId", "profileType", "totalCountOfLatestAttributes"]
    #     )

    # TODO Link the commit history
    # Todo .. pull changes on profile as of latest commit ...
    #     Net attributes added ... download them and append them to the profile ..

    # def findProfilesWithAllAttributes(self, attributeKeys:List[str]):
    #     """
    #     Returns a list of profiles that have all of the attributes specified in their latest version.
    #     :param attributeKeys:
    #     :return:
    #     """
    #     pass
    #
    # def findProfilesWithSomeAttributes(self, attributeKeys:List[str]):
    #     """
    #     Returns a list of profiles that have all of the attributes specified in their latest version.
    #     :param attributeKeys:
    #     :return:
    #     """
    #     pass

    # def findProfilesWithAttributeQuery(self):


    # def findsCommitsBetweenDates

    # Todo link to find attributes ...
    # Todo ... link to ... find_latest_snapshot_for_profile
    # TODO - link to find query commits  in internal ......
    # TODO .. link to interla find profiles ...

    # def list_available_attributes_for_latest_profile(self, profileId: str) -> List[ProfileAttributeMapping]:
    #     # snapshot = find_latest_snapshot_for_profile(profileId, cortex)
    #     # if not snapshot:
    #     #     return []
    #     # return list(map(
    #     #     lambda attr: ProfileAttributeMapping(attributeKey=attr.attributeKey, attributeId=attr.id),
    #     #     snapshot.attributes
    #     # ))
    #     return [
    #         ProfileAttributeMapping(attributeKey=attribute.attributeKey, attributeId=attribute.id)
    #         for attribute in self._internal_profiles_client.find_latest_attributes_for_profile(profileId, [])
    #     ]

    # When we get history of a profile ...
    #   ... we get the latest commit for that profile and find all of the commits it was recursively involved in
    #   ... and get the commit id and time of each !
    # We can even turn this into a dataframe!


    # def merge_attributes_with_profile():
    #     """
    #     This attempts to merge two sets of profiles
    #     i.e ... two counters will get merged ...
    #     counters get merged ...
    #     latest is chosen for declared attributes ...
    #     :return:
    #     """
    #     pass


    # def net_attributes_from_commit_chain(commitChain: ProfileCommitChain) -> List[ProfileAttributeMapping]:
    #     """
    #     What are the net profile attributes after applying all of the changes
    #     in the commit chain?
    #     """
    #     snapshot = commitChain.snapshot
    #     # Start with attribute from profile snapshots ...
    #     attributes = snapshot.attributes
    #
    #     # Apply all of the additional commits on top of the snapshot ...
    #     attributes = flatmap(commitChain.additionalCommits, attributes, apply_commit_to_attributes)
    #     # Apply the latest commit
    #     attributes = apply_commit_to_attributes(attributes, )


    # def get_current_profile_attributes_for_user(profileId):
    #     pass

if __name__ == '__main__':
    pc = ProfilesClient.from_current_cli_profile()
    print(pc.describeProfile("27504729-3958-4911-930f-74b19d7a8e29", "cortex/schema:13"))