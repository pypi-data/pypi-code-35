#!/usr/bin/env python
try:
    import simplejson as json
except ImportError:
    import json

class Service(object):
    """OAuth 2.0 service provider e.g. Facebook, Google. It takes
    endpoint urls for authorization and access token gathering APIs.

    :param authorize_endpoint: api url for authorization
    :type authorize_endpoint: :class:`basestring`
    :param access_token_endpoint: api url for getting access token
    :type access_token_endpoint: :class:`basestring`

    """

    #: (:class:`basestring`) The API URL for authorization.
    authorize_endpoint = None

    #: (:class:`basestring`) The API URL for getting access token.
    access_token_endpoint = None

    def __init__(self, authorize_endpoint, access_token_endpoint):
        def check_endpoint(endpoint):
            if not isinstance(endpoint, str):
                raise TypeError('endpoint must be a string, not ' +
                                repr(endpoint))
            elif not (endpoint.startswith('http://') or
                      endpoint.startswith('https://')):
                raise ValueError('endpoint must be a url string, not ' +
                                 repr(endpoint))
            return endpoint
        self.authorize_endpoint = check_endpoint(authorize_endpoint)
        self.access_token_endpoint = check_endpoint(access_token_endpoint)

    def load_username(self, access_token):
        """Load a username from the service suitable for the REMOTE_USER
        variable. A valid :class:`AccessToken` is provided to allow access to
        authenticated resources provided by the service. If the service supports
        usernames this method must set the 'username' parameter to access_token.

        :param access_token: a valid :class:`AccessToken`

        .. versionadded:: 0.1.2

        """
        #raise NotImplementedError(
        #    "This Service does not provide a username for REMOTE_USER")
        response = access_token.get('https://www.googleapis.com/oauth2/v2/userinfo')
        #response = response.read()
        response = json.loads(response)
        # Copy useful data
        #access_token["username"] = response["login"]
        access_token["name"] = response["name"]
        access_token["email"] = response["email"]       


    def is_user_allowed(self, access_token):
        """Check if the authenticated user is allowed to access the protected
        application. By default, any authenticated user is allowed access.
        Override this check to allow the :class:`Service` to further-restrict
        access based on additional information known by the service.

        :param access_token: a valid :class:`AccessToken`

        .. versionadded:: 0.1.3

        """
        return True

class GitHubService(Service):
    """OAuth 2.0 service provider for GitHub with support for getting the
    authorized username.

    :param allowed_orgs: What GitHub Organizations are allowed to access the
                         protected application.
    :type allowed_orgs: :class:`basestring`,
                        :class:`collections.Container` of :class:`basestring`

    .. versionadded:: 0.1.3
       The ``allowed_orgs`` option.

    .. versionadded:: 0.1.2

    """

    def __init__(self, allowed_orgs=None):
        super(GitHubService, self).__init__(
            authorize_endpoint='https://github.com/login/oauth/authorize',
            access_token_endpoint='https://github.com/login/oauth/access_token')
        # coerce a single string into a list
        if isinstance(allowed_orgs, str):
            allowed_orgs = [allowed_orgs]
        self.allowed_orgs = allowed_orgs

    def load_username(self, access_token):
        """Load a username from the service suitable for the REMOTE_USER
        variable. A valid :class:`AccessToken` is provided to allow access to
        authenticated resources provided by the service. For GitHub the 'login'
        variable is used.

        :param access_token: a valid :class:`AccessToken`

        .. versionadded:: 0.1.2

        """
        response = access_token.get('https://api.github.com/user')
        response = response.read()
        response = json.loads(response)
        # Copy useful data
        access_token["username"] = response["login"]
        access_token["name"] = response["name"]

    def is_user_allowed(self, access_token):
        """Check if the authenticated user is allowed to access the protected
        application. If this :class:`GitHubService` was created with a list of
        allowed_orgs, the user must be a memeber of one or more of the
        allowed_orgs to get access. If no allowed_orgs were specified, all
        authenticated users will be allowed.

        :param access_token: a valid :class:`AccessToken`

        .. versionadded:: 0.1.3

        """
        # if there is no list of allowed organizations, any authenticated user
        # is allowed.
        if not self.allowed_orgs:
            return True

        # Get a list of organizations for the authenticated user
        response = access_token.get("https://api.github.com/user/orgs")
        response = response.read()
        response = json.loads(response)
        user_orgs = set(org["login"] for org in response)

        allowed_orgs = set(self.allowed_orgs)
        # If any orgs overlap, allow the user.
        return bool(allowed_orgs.intersection(user_orgs))


GithubService = GitHubService



#: (:class:`Service`) The predefined service for Facebook__.
#:
#: __ https://www.facebook.com/
facebook = Service(
    authorize_endpoint='https://www.facebook.com/dialog/oauth',
    access_token_endpoint='https://graph.facebook.com/oauth/access_token'
)

#: (:class:`Service`) The predefined service for Google__.
#:
#: __ http://www.google.com/
google = Service(
    authorize_endpoint='https://accounts.google.com/o/oauth2/auth',
    access_token_endpoint='https://accounts.google.com/o/oauth2/token'
)

#: (:class:`GitHubService`) The predefined service for GitHub__.
#:
#: .. versionadded:: 0.1.2
#:
#: __ https://github.com/
github = GitHubService()
