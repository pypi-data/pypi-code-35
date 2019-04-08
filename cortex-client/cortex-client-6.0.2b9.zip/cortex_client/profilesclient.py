
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

import traceback
import urllib
from typing import List, Optional, cast

import arrow
import deprecation
import pydash
from cortex_client.client import _Client
from cortex_common.types import MessageResponse, Profile, ProfileSchema, EntityEvent, ProfileSummary, \
    DeclaredProfileAttribute, ProfileAttributeType, EntityAttributeValue, ProfileVersionSummary, \
    ProfileAttributeSummary, HistoricProfile
from cortex_common.utils import head, dicts_to_classes, dict_to_attr_class, construct_attr_class_from_dict, \
    utc_timestamp, fold_list
from requests.exceptions import HTTPError

from .utils import get_logger

OrderedList = List
NoneType = type(None)
log = get_logger(__name__)

class ProfilesClient(_Client):
    """A client for the Cortex Profiles SDK Functionality."""

    URIs = {
        'events': 'graph/events/entities',
        'profiles': 'graph/profiles',
        'schemas': 'graph/profiles/schemas',
        'schema':  'graph/profiles/schemas/{schemaId}',
        'profile': 'graph/profiles/{profileId}',
    }

    @classmethod
    def build_get_profile_uri(cls, profileId:str, schemaId:str, historic:bool=False, version:Optional[str]=None):
        url_args = pydash.merge(
            {"historic": str(historic).lower()},  # Python turns True:bool into True:str
            {} if schemaId is None else {"schemaNames": schemaId},
            {} if version is None else {"version": version}
        )
        return "{}?{}".format(cls.URIs["profile"].format(profileId=profileId), urllib.parse.urlencode(url_args))

    def __init__(self, url, version, token):
        super(ProfilesClient, self).__init__(url, version, token)

    def findProfiles(self, query:Optional[dict]={}) -> List[ProfileSummary]:
        """
        Finding profiles in the system.

        :param query: An optional mongo-oritented query that can reduce the amount of profiles found.
        :return:
        """
        profiles = self._get_json(self.URIs["profiles"])["profiles"]
        return fold_list(dicts_to_classes(profiles, ProfileSummary))

    def listSchemas(self) -> List[ProfileSchema]:
        """
        List all of the schemas currently loaded into the system.
        :return:
        """
        uri = self.URIs["schemas"]
        print("Requesting {}".format(uri))
        schemas = self._get_json(uri)["schemas"]
        print("Done Requesting {}".format(uri))
        return fold_list(dicts_to_classes(schemas, ProfileSchema))

    def pushSchema(self, schema:ProfileSchema) -> MessageResponse:
        return MessageResponse(**self._post_json(self.URIs["schemas"], dict(schema)))  # type: ignore

    def describeSchema(self, schemaId:str, version:Optional[str]=None) -> Optional[ProfileSchema]:
        """
        >>> describeSchema("cortex/end-user")
        :param schemaId: The name of the schema we are interested in describinb.
        :param version: By default, the latest version of the schema is returned, otherwise, the version indicated.
        :return: The profile schema if found, otherwise None.
        """
        try:
            uri = self.URIs["schema"].format(schemaId=schemaId)
            print("Requesting {}".format(uri))
            schema = self._get_json(uri)
            print("Done requesting {}".format(uri))
        except Exception as e:
            print(e)
            return None
        returnVal = dict_to_attr_class(schema, ProfileSchema)
        return returnVal

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

    def _get_profile(self, profileId:str, schemaId:Optional[str], historic:Optional[bool]=False, version:Optional[str]=None) -> List[dict]:
        """
        Gets a profile using the cortex-graph api ...

        :param profileId:
        :param schemaId: What schema are we interested in retreiving the profile for the entity for?
        :param historic: Do we want to get all of the historic attributes for the profile. By default only latest are returned.
        :param version: At what specific version did we want to retreive the profile?
        :return:
        """
        uri = ProfilesClient.build_get_profile_uri(profileId, schemaId, historic=historic, version=version)
        print("Requesting {}".format(uri))
        raw_profiles = self._get_json(uri)
        print("Done with request to {}".format(uri))
        return raw_profiles.get("profiles", [])

    def describeHistoricProfile(
            self, profileId: str, schemaId: str, version: Optional[str] = None) -> Optional[HistoricProfile]:
        """
        Get the profile at a specific version with attributes that contain all of their historic values ...

        :param profileId:
        :param schemaIds: What schemas do we want to get the profile for ...?
        :param version: What version do we want to limit the profile to?
        :return:
        """
        if schemaId is None:
            raise Exception("schemaId required.")
        try:
            profile = head(self._get_profile(profileId, schemaId, historic=True, version=version))
            p = dict_to_attr_class(profile, HistoricProfile)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            p = None
        return p

    def describeProfile(
            self, profileId:str, schemaId:str, version:Optional[str]=None) -> Optional[Profile]:
        """
        Get the profile at a specific version ... only latest values of attributes are provided ...

        :param profileId:
        :param schemaIds: What schemas do we want to get the profile for ...?
        :param version: What version do we want to limit the profile to?
        :return:
        """
        if schemaId is None:
            raise Exception("schemaId required.")
        try:
            profile = head(self._get_profile(profileId, schemaId, historic=False, version=version))
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
        print(response)
        return [
            r.get("message") for r in response
        ]

    @deprecation.deprecated(deprecated_in='6.0.1b1', details='Use pushEvents instead.')
    def pushAttributes(self, profileId:str, attributes:List[ProfileAttributeType]) -> List[str]:
        """
        Pushes attributes to the latest profile for the specified profileId.
        Returns a list of messages with regards to the status of each attribute being pushed ...

        :param profileId:
        :param attributes:
        :return:
        """
        return fold_list(self.pushEvents([
            self._turn_attribute_into_entity_event(a) for a in attributes
        ]))

    def _turn_attribute_into_entity_event(self, attribute:ProfileAttributeType) -> EntityEvent:
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
            return EntityEvent(  # type: ignore
                event=attribute.attributeKey,
                entityId=attribute.profileId,
                entityType=attribute.profileSchema,
                eventTime=attribute.createdAt,
                properties=dict(attribute.attributeValue)
            )

    def _turn_entity_event_into_attribute(
            self, entityEvent:EntityEvent, attributeType:type=DeclaredProfileAttribute, attributeValueType:type=EntityAttributeValue) -> ProfileAttributeType:
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
                createdAt=arrow.get(cast(int, entityEvent.eventTime) / 1000),
            )
        else:
            return attributeType(
                profileId=entityEvent.entityId,
                profileSchema=entityEvent.entityType,
                attributeKey=entityEvent.event,
                attributeValue=construct_attr_class_from_dict(attributeValueType, entityEvent.properties),
                createdAt=arrow.get(cast(int, entityEvent.eventTime)/1000) if entityEvent.eventTime is not None else utc_timestamp(),
            )

    def describeAttributeByKey(self, profileId: str, schemaId: str, attributeKey: str) -> Optional[ProfileAttributeType]:
        """
        Describe a specific attribute in the profile ...
        Either attributeId or attributeKey must be provided ... attributeId takes precedence over attributeKey ...
        If attribute key is provided ... the

        commitId: Optional[str] = None

        TODO ... implement this on the server end ...

        :param profileId:
        :param attributeKey:
        :param commitId:
        :return:
        """
        profile = self.describeProfile(profileId, schemaId)
        if profile is None:
            return None
        return head([a for a in profile.attributes if a.attributeKey == attributeKey])

    # PHASE 2 - Move the following to the server side!

    def listVersions(self, profileId:str, schemaId:str) -> List[ProfileVersionSummary]:
        """
        Lists all of the modifications done on the profile ... with the date of each modification!
        Currently this gets the entire historic profile to determine the commits on the profile ...
        This should be moved to the server side, and the cortex-graph service should have an api to list the different
        version for each of the profiles.

        :param profileId:
        :return:
        """
        historic_profile = head(self._get_profile(profileId, schemaId, historic=True))
        historic_attributes = historic_profile.get("attributes", [])
        # Get a map of all the versions as the keys and the time at which they were created as their values
        version_time_map = pydash.merge({},{},*[
            dict(zip(historic_attr["seqs"], historic_attr["timeline"]))
            for historic_attr in historic_attributes
        ]) # Merging two empty dicts together to not error out just incase there are no historic attributes ...
        return sorted([
            ProfileVersionSummary(
                profileId=profileId,
                schemaId=schemaId,
                version=version,
                createdAt=timestamp
            )
            for version, timestamp in version_time_map.items()
        ], key=lambda x: -1 * x.version)

    def listAttributes(self, profileId: str, schemaId:str, version:Optional[str]=None) -> Optional[List[ProfileAttributeSummary]]:
        """
        List all of the attributes currently contained in a profile that adheres to a specific schema ...
            ... defaults to latest commit if no commitId is specified ...
        :param profileId:
        :param commitId:
        :return:
        """
        historic_profile = head(self._get_profile(profileId, schemaId, historic=True, version=version))
        print(historic_profile)
        # For each attribute, figure out the first time the value was modified ... and the last time it was modified ..
        return sorted([
            ProfileAttributeSummary(
                profileId=profileId,
                schemaId=schemaId,
                attributeKey=attribute["attributeKey"],
                attributeType=attribute["attributeContext"],
                attributeValueType=head(attribute["attributeValues"])["context"],
                createdAt=min(attribute["timeline"]),
                updatedAt=max(attribute["timeline"])
            )
            for attribute in historic_profile.get("attributes", [])
        ], key=lambda x: x.attributeKey)

    # PHASE 3

    # def describeCommit(self, commitId:str):
    #     """
    #     Describe a specific commit ...
    #     :param commitId:
    #     :return:
    #     """
    #     return self._internal_profiles_client.get_commit_by_id(commitId)

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

    # TODO ... do we want to expose an id per attribute ... or does one request an attribute at a specific version of a profile?
    # def describeAttributeById(self, attributeId:str) -> Optional[ProfileAttribute]:
    #     """
    #     Describe a specific attribute in the profile ...
    #     Either attributeId or attributeKey must be provided ... attributeId takes precedence over attributeKey ...
    #     If attribute key is provided ... the
    #     :param attributeId:
    #     :return:
    #     """
    #     return self._internal_profiles_client.get_attribute_by_id(attributeId)

if __name__ == '__main__':
    pc = ProfilesClient.from_current_cli_profile()
    # print(pc.describeProfile("27504729-3958-4911-930f-74b19d7a8e29", "cortex/schema:13"))
    print(pc.listVersions("983jf74t", "cortex/FinancialCustomer:1"))
    print(pc.listAttributes("983jf74t", "cortex/FinancialCustomer:1"))