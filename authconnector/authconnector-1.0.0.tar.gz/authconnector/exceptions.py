from rest_framework.exceptions import APIException
from rest_framework import status


class UserInfoRetrievalFailed(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'An error happened while trying to retrieve the user information.'
    default_code = 'jwt_authentication_failure'


class AuthServiceResponseFailed(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = 'It was impossible to contact the authentication service. Please contact the administrator.'
    default_code = 'auth_service_response_failure'
