import base64
import json
import time
import unittest
from typing import List, Callable, Union

import pandas as pd
from mocket import mocketize
from mocket.mockhttp import Entry

from cortex.builder.declared_attributes_builder import DeclaredAttributesBuilder
from cortex.profile.constants.contexts import ATTRIBUTES, ATTRIBUTE_VALUES
from cortex.profile.types import EntityEvent, Profile, ProfileSchema, ProfileAttributeSchema, ProfileValueTypeSummary, \
    ProfileAttributeType, DeclaredProfileAttribute, StringAttributeValue, IntegerAttributeValue
from cortex.profile.utils import unique_id, head
from cortex_client.profilesclient import ProfilesClient
from .fixtures import john_doe_token, build_mock_url, mock_api_endpoint


class TestAgent(unittest.TestCase):

    def register_entry(self, verb, url, body:dict):
        print('Registering mock for', verb, url)
        Entry.single_register(verb, url, status=200, body=json.dumps(body))

    def register_entry_from_path(self, verb, url, path:str):
        with open(path) as fh:
            self.register_entry(verb, url, json.load(fh))

    def setUp(self):
        # Register Cortex Next Secret ...
        next_secret = json.dumps({
            "url": mock_api_endpoint(),
            "token": john_doe_token(),
            "username": "username",
            "password": base64.b64encode("password".encode("utf-8")).decode("utf-8")
        })
        self.register_entry(
            Entry.GET, build_mock_url("tenants/secrets/cortex-next", version=2), {
                "some-key": base64.b64encode(next_secret.encode("utf-8")).decode("utf-8")
            }
        )

        # Registering List Schemas ...
        self.register_entry_from_path(
            Entry.GET, build_mock_url("graph/profiles/schemas", version=3), "./test/data/apis/profiles/schemas/list_schemas.json"
        )

        self.cli_based_profile_client = ProfilesClient.from_current_cli_profile()

        self.profile_id = unique_id()

        self.valid_string_event = EntityEvent(
            event="profile.name",
            entityId=self.profile_id,
            entityType="cortex/profile-of-end-user",
            properties={
                "value": "Jack"
            }
        )

        self.valid_entity_event = EntityEvent(
            event="entity-attribute",
            entityId=self.profile_id,
            entityType="cortex/profile-of-end-user",
            properties={
                "p1": "some-property-value",
                "p2": 2
            }
        )

        self.valid_schema = ProfileSchema(
            name="cortex/schema",
            title="cortex/schema",
            description="A Simple Schema",
            attributes=[
                ProfileAttributeSchema(
                    name="profile.name",
                    type=ATTRIBUTES.DECLARED_PROFILE_ATTRIBUTE,
                    valueType=ProfileValueTypeSummary(outerType=ATTRIBUTE_VALUES.STRING_PROFILE_ATTRIBUTE_VALUE),
                    label="profile.name",
                    description="profile.name"
                ),
                ProfileAttributeSchema(
                    name="profile.age",
                    type=ATTRIBUTES.DECLARED_PROFILE_ATTRIBUTE,
                    valueType=ProfileValueTypeSummary(outerType=ATTRIBUTE_VALUES.INTEGER_PROFILE_ATTRIBUTE_VALUE),
                    label="profile.name",
                    description="profile.name"
                ),
                ProfileAttributeSchema(
                    name="entity-attribute",
                    type=ATTRIBUTES.DECLARED_PROFILE_ATTRIBUTE,
                    label="entity-attribute",
                    valueType=ProfileValueTypeSummary(outerType=ATTRIBUTE_VALUES.ENTITY_ATTRIBUTE_VALUE),
                    description="entity-attribute"
                )
            ]
        )

        self.cli_based_profile_client.deleteProfile(self.profile_id)
        self.cli_based_profile_client.deleteSchema(self.valid_schema.name)

    @mocketize
    def test_get_mock_schemas(self):
        """
        Tests getting schemas from a mocked endpoint ...
        :return:
        """
        schemas = ProfilesClient(mock_api_endpoint(), "3", john_doe_token()).listSchemas()
        self.assertEqual(len(schemas), 1)
        self.assertEqual(schemas[0].name, "cortex/Account")

    def _test_building_profile(
            self,
            schema_to_use:ProfileSchema,
            items_to_push:List[Union[EntityEvent, ProfileAttributeType]],
            function_to_push:Callable
    ):
        """
        Helper Method to
        :param schema_to_use:
        :param items_to_push:
        :param function_to_push:
        :return:
        """

        # Push a new schema ...
        self.cli_based_profile_client.pushSchema(schema_to_use)

        # Get latest version of the schema ...
        latest_schema_id = "{}:{}".format(
            schema_to_use.name,
            self.cli_based_profile_client.describeSchema(schema_to_use.name)._version
        )
        print("Latest Schema after push: {}".format(latest_schema_id))

        # Push Events that adhere to the schema ...
        responses = function_to_push(items_to_push)
        print(responses)
        self.assertEqual(len(responses), len(items_to_push), "Valid response to push events.")
        self.assertTrue(None not in responses, "Valid response to push events.")

        # Wait for Event to lead to creation of attribute
        # TODO ... figure out on average how long it takes an attribute to be added to a profile after an entity event is pushed ...
        time.sleep(1)

        # Get the profile at the specific version ...
        profile = self.cli_based_profile_client.describeProfile(self.profile_id, latest_schema_id)
        self.assertIsInstance(profile, Profile, "Successfully get Proifile from API.")
        attribute_from_event = head([a for a in profile.attributes if a.attributeKey == self.valid_string_event.event])

        # Get the
        self.assertEqual(
            attribute_from_event.attributeValue.value, self.valid_string_event.properties["value"],
            "The attribute should contain value from event ..."
        )

    def test_pushing_events(self):
        self._test_building_profile(
            self.valid_schema, [self.valid_string_event], self.cli_based_profile_client.pushEvents,
        )

    def test_pushing_attributes(self):
        attributes_to_push = [
            self.cli_based_profile_client._turn_entity_event_into_attribute(
                self.valid_string_event, DeclaredProfileAttribute, StringAttributeValue
            )
        ]
        self._test_building_profile(
            self.valid_schema,
            attributes_to_push,
            lambda attributes: self.cli_based_profile_client.pushAttributes("doesnt-matter", attributes),
        )

    def test_pushing_attributes_built_with_builder(self):
        builder = DeclaredAttributesBuilder()
        builder.append_attributes_from_kv_df(
            pd.DataFrame([
                {"profileId": self.profile_id, "key": "profile.name", "value": self.valid_string_event.properties["value"]},
            ]),
            self.valid_schema.name,
            attribute_value_class=StringAttributeValue
        )
        builder.append_attributes_from_column_in_df(
            pd.DataFrame([
                {"profileId": self.profile_id, "age": 20},
            ]),
            self.valid_schema.name,
            key="profile.age",
            value_column="age",
            attribute_value_class=IntegerAttributeValue
        )
        attributes_to_push = builder.get()
        self._test_building_profile(
            self.valid_schema,
            attributes_to_push,
            lambda attributes: self.cli_based_profile_client.pushAttributes("doesnt-matter", attributes),
        )

    # TODO ... make sure schema versions increment ...
    # TODO ... Pushing events asyncly and seeing if the profile is consistently built ...

    def test_parsing_attributes(self):
        attrs = [
            {
                "attributeKey": "account.properties",
                "id": "68cd1c62-8a71-4203-a1a3-a1fed40a3171",
                "profileId": self.profile_id,
                "profileSchema": "cortex/TestSchema:2",
                "classification": "declared",
                "attributeValue": {
                    "context": "cortex/attribute-value-entity",
                    "version": "0.0.1",
                    "value": {
                        "event": "age",
                        "entityId": "abc",
                        "entityType": "cortex/blah",
                        "properties": {
                            "p1": "some-string",
                            "p2": 123
                        }
                    }
                },
                "createdAt": "2019-03-22T22:06:17.058Z",
                "version": "0.0.1",
                "seq": 21,
                "context": "cortex/attributes-declared"
            }
        ]
        from cortex.profile.utils.attr_utils import dicts_to_classes
        from cortex.profile.types.attributes import ProfileAttributeType, load_profile_attribute_from_dict
        print(dicts_to_classes(attrs, ProfileAttributeType, dict_constructor=load_profile_attribute_from_dict))

    def test_parsing_events(self):
        event = self.valid_string_event
        from cortex.profile.utils.attr_utils import dict_to_attr_class
        print(dict_to_attr_class(event, EntityEvent))
