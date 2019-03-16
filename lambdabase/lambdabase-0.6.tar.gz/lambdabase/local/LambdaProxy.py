import simplejson as json
import uuid
from flask import Response


class LambdaProxy(object):
    """
    Maps flask requests into the format
    used by API gateways lambda proxy3
    """
    def __init__(self, cognito_proxy=None):
        self.cognito_proxy = cognito_proxy

    def map(self, request):
        """
        Maps flask request object into the format
        expected by a lambda request via the lambda
        proxy used by API gateway
        :param request: a flask request object
        :return: the resultant lambda proxy formatted request
        """
        headers = dict(request.headers)
        event = {
            "headers": headers,
            "path": request.path,
            "pathParameters": request.view_args,
            "requestContext": {"httpMethod": request.method},
            "queryStringParameters": request.args.to_dict(flat=False),
            "body": json.loads(request.data) if request.data else {},
            "context": {'correlation_id': str(uuid.uuid4())}
        }

        if 'Authorization' in headers:
            claims = self.cognito_proxy.get_claims(headers.get('Authorization'))
            event.get('requestContext')['authorizer'] = {}
            event['requestContext']['authorizer']['claims'] = claims

        return event

    @classmethod
    def unmap(cls, response):
        headers = response.get('headers')
        body = json.loads(response.get('body'))
        code = response.get('statusCode')

        resp = Response(headers=headers, status=code, mimetype='application/json')
        resp.data = json.dumps(body)
        return resp




