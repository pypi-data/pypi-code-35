import uuid
from lambdabase.Request import AuthenticatedRequest


class RequestContext(object):
    """
    Context object for storing transient information related to each request
    """
    user_id = 'anonymous'
    request_id = 'none'
    correlation_id = 'none'

    @classmethod
    def set(cls, request, context):
        """
        Build the internal request from input parameters
        1. Get the request id from the context
        2. Get the correlation id if present or
            generate a new one if not present
        3. Get the user id from the context if possible
            (lambda to lambda call) or from the claims object
            (api gateway authenticated call) or leave as
            anonymous if the call isn't authenticated.
        """
        cls.request_id = context.aws_request_id

        if request.correlation_id is not None:
            cls.correlation_id = request.correlation_id
        else:
            cls.correlation_id = str(uuid.uuid4())

        if isinstance(request, AuthenticatedRequest):
            cls.user_id = request.user_id

    @classmethod
    def reset(cls):
        """
        Revert settings to their default at the
        end of the request
        """
        cls.user_id = 'anonymous'
        cls.request_id = 'none'
        cls.correlation_id = 'none'
