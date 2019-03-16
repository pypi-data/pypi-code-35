from lambdabase.local.JwtValidator import JwtValidator


class CognitoProxy(object):
    """
    Local proxy class for cognito. Handles inserting validated claims into
    the authenticated requests for use as part of the AuthenticatedRequest
    """
    validator = JwtValidator()

    def __init__(self, aws_region, aws_user_pool, client_id):
        """
        Initialise the proxy with constant values
        :param aws_region: the aws region
        :param aws_user_pool: the user pool id
        :param client_id: the user pool client id
        """
        self.aws_region = aws_region
        self.aws_user_pool = aws_user_pool
        self.client_id = client_id

    def get_claims(self, token):
        """
        :return: returns the claims object based on the passed jwt token
        """
        return self.validator.get_claims(self.aws_region, self.aws_user_pool,
                                         token, self.client_id)
