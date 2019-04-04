from allauth.socialaccount import providers
from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth2.provider import OAuth2Provider


class iHelaAccount(ProviderAccount):
    pass


class iHelaProvider(OAuth2Provider):

    id = "ihelaprovider"
    name = "iHela Plateform OAuth2 Provider"
    account_class = iHelaAccount

    def extract_uid(self, data):
        # print(data)
        return str(data["id"])

    def extract_common_fields(self, data):
        from pprint import pprint

        return dict(
            username=data["username"],
            email=data["email"],
            # first_name=data["first_name"],
            # last_name=data["last_name"],
        )

    def get_default_scope(self):
        scope = ["read"]
        return scope


providers.registry.register(iHelaProvider)
