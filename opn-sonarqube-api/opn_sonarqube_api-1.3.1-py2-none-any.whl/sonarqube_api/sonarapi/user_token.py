class SonarAPIUserToken(object):
    #Endpoint for permission templates
    USER_TOKEN_GENERATE_ENDPOINT = '/api/user_tokens/generate'

    def __init__(self, api=None):
        self._api = api

    def generate_token(self, token_name, user_login):
        """
        Create template.

        :param token_name: name of the token to generate
        :param user_login: user to generate token for
        :return: request response
        """
        # Build main data to post
        data = {
            'name': token_name,
            'login': user_login
        }

        # Make call (might raise exception) and return
        res = self._api._make_call('post', self.USER_TOKEN_GENERATE_ENDPOINT, **data)
        return res