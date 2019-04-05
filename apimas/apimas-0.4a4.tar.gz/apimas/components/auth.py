from apimas.errors import UnauthorizedError
from apimas.base import ProcessorFactory
from apimas.auth import MissingCredentials
from apimas import utils


class Authentication(ProcessorFactory):
    """
    Processor for performing authentication based on a selected method.
    """

    authenticator = None

    def __init__(self, collection_loc, action_name, authenticator, verifier):

        if authenticator:
            assert verifier
            verifier = utils.import_object(verifier)
            _cls = utils.import_object(authenticator)
            self.authenticator = _cls(verifier)

    def process(self, data):
        if self.authenticator is None:
            # If there is not any constructed authentication backend, then
            # we presume that the collection is not protrected, so we skip
            # this processor.
            return {'auth/identity': None}

        try:
            return {
                'auth/identity': self.authenticator.authenticate(
                    data['request/meta/headers'])
            }
        except MissingCredentials:
            # this indicates anonymous access, permissions processor will
            # handle authorization for this request
            return {'auth/identity': None}
        except UnauthorizedError as exc:
            # Provide the appropriate headers, so that handler can read them
            # later.
            auth_headers = getattr(self.authenticator, 'AUTH_HEADERS', None)
            if auth_headers:
                exc.response_headers = {'WWW-Authenticate': auth_headers}
            raise exc


class UserRetrieval(ProcessorFactory):
    ANONYMOUS_ROLE = 'anonymous'
    ROLE_HEADER = 'USER_ROLE'

    def __init__(self, collection_loc, action_name, user_resolver=None):
        if user_resolver:
            user_resolver = utils.import_object(user_resolver)
            assert callable(user_resolver), (
                '"user_resolver" must be a callable')
        self.user_resolver = user_resolver

    def process(self, data):
        runtime = data['$runtime']
        headers = data.get('request/meta/headers')
        identity = data.get('auth/identity')

        if not identity:
            user = None
        else:
            if not self.user_resolver:
                raise Exception("No user_resolver set")
            user = self.user_resolver(identity, runtime)

        if user is None:
            role = self.ANONYMOUS_ROLE
        else:
            role = headers.get(self.ROLE_HEADER)

        if role != self.ANONYMOUS_ROLE:
            user_roles = getattr(user, 'apimas_roles', None)
            assert user_roles is not None, (
                'Cannot find property `apimas_roles` on `user` object')
            if role is not None:
                if role not in user_roles:
                    raise UnauthorizedError(
                        "User does not have role '%s'" % role)
            else:
                role = user_roles[0]

        return {'auth/user': user, 'auth/role': role}
