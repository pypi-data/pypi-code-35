import base64
import json
import unittest

from mocket import mocketize
from mocket.mockhttp import Entry

from cortex_client.profilesclient import ProfilesClient
from cortex.profile.types.schemas import ProfileSchema, ProfileAttributeSchema, ProfileValueTypeSummary
from cortex.profile.constants.contexts import ATTRIBUTES, ATTRIBUTE_VALUES
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

        self.profile_client = ProfilesClient.from_current_cli_profile()

        self.valid_schema = ProfileSchema(
            name="cortex/EmptySchema",
            title="cortex/EmptySchema",
            description="An Empty Profile",
            attributes=[
                ProfileAttributeSchema(
                    name="simple.attribute",
                    type=ATTRIBUTES.DECLARED_PROFILE_ATTRIBUTE,
                    valueType=ProfileValueTypeSummary(outerType=ATTRIBUTE_VALUES.STRING_PROFILE_ATTRIBUTE_VALUE),
                    label="simple.attribute",
                    description="simple.attribute"
                )
            ]
        )

    @mocketize
    def test_get_schemas(self):
        schemas = ProfilesClient(mock_api_endpoint(), "3", john_doe_token()).listSchemas()
        self.assertEqual(len(schemas), 1)
        self.assertEqual(schemas[0].name, "cortex/Account")

    def test_push_schema(self):
        """
        Pushing a simple schema ... twice ... and ensuring its version increments ...
        :return:
        """

        first_version = self.profile_client.pushSchema(self.valid_schema).version
        second_version = self.profile_client.pushSchema(self.valid_schema).version

        print(self.profile_client.describeSchema(self.valid_schema.name))
        self.assertEqual(first_version + 1, second_version)

    def test_describe_things_that_doesnt_exist(self):
        """
        Ensures we dont crash if we try to describe things that dont exist ...
        :return:
        """

        # Getting a none existent schema should return None ...
        self.assertIsNone(self.profile_client.describeSchema("cortex/i_dont_exist"))

        # Getting an existent agent should return the agent ...
        self.profile_client.pushSchema(self.valid_schema)
        self.assertIsNotNone(self.profile_client.describeSchema("cortex/EmptySchema"))
        self.assertIsInstance(self.profile_client.describeSchema("cortex/EmptySchema"), ProfileSchema)

    def test_delete_things(self):
        self.profile_client.pushSchema(self.valid_schema)
        self.assertIs(self.profile_client.deleteSchema(self.valid_schema.name), True)

    def test_delete_things_that_dont_exist(self):
        self.assertIs(self.profile_client.deleteSchema(self.valid_schema.name), False)
        self.assertIs(self.profile_client.deleteSchema(self.valid_schema.name), False)
        # TODO ... the above should return a 400 ... not a 500
        pass


    def test_parsing_types(self):
        print(
            ProfileValueTypeSummary(**{
                "outerType": "str",
                "innerTypes": []
            })
        )
        print(
            ProfileValueTypeSummary(**{
                "outerType": "map",
                "innerTypes": [
                    {
                        "outerType": "str",
                        "innerTypes": []
                    },
                    {
                        "outerType": "int",
                        "innerTypes": []
                    }
                ]
            })
        )
        print(
            ProfileValueTypeSummary(**{
                "outerType": "map",
                "innerTypes": [
                    {
                        "outerType": "str",
                        "innerTypes": []
                    },
                    {
                        "outerType": "list",
                        "innerTypes": [
                            {
                                "outerType": "int",
                                "innerTypes": []
                            }
                        ]
                    }
                ]
            })
        )