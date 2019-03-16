import requests
import json as json
from jose import jwt


class JwtValidator(object):
    """
    Validate a JWT token and extract the claims from within
    """
    _aws_key_dict = None

    def get_claims(self, aws_region, aws_user_pool, token, audience=None):
        """ Given a token (and optionally an audience), validate and
        return the claims for the token
        """
        header = jwt.get_unverified_header(token)
        kid = header['kid']
        verify_url = self.pool_url(aws_region, aws_user_pool)
        keys = self.aws_key_dict(aws_region, aws_user_pool)
        key = keys.get(kid)

        kargs = {"issuer": verify_url}
        if audience is not None:
            kargs["audience"] = audience

        return jwt.decode(token, key, **kargs)

    @classmethod
    def pool_url(cls, aws_region, aws_user_pool):
        """
        Create an Amazon cognito issuer URL from a region and pool id
        """
        return "https://cognito-idp.{}.amazonaws.com/{}".format(aws_region, aws_user_pool)

    def aws_key_dict(self, aws_region, aws_user_pool):
        """
        Fetches the AWS JWT validation file (if necessary) and then converts
        this file into a keyed dictionary that can be used to validate a web-token
        we've been passed
        """
        if not self._aws_key_dict:
            aws_data = requests.get(self.pool_url(aws_region, aws_user_pool) + '/.well-known/jwks.json')
            aws_jwt = json.loads(aws_data.text)

            result = {}
            for item in aws_jwt['keys']:
                result[item['kid']] = item
            self._aws_key_dict = result
        return self._aws_key_dict
