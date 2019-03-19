"""Recommender API class file."""

from google.auth.transport.requests import AuthorizedSession


class Recommender(object):
    """Recommender class."""

    def __init__(self, credentials):
        """Initialize a class instance."""
        self.api_version = 'v1alpha1'
        self.base_url = 'https://recommender.googleapis.com/%s' % (
            self.api_version,
        )
        self.credentials = credentials
        self.requests = AuthorizedSession(self.credentials)

    def get_role_recommendations(self, resource):
        """Return role recommendations for a resource."""
        recommender = 'google.iam.policy.RoleRecommender'
        url = '%s/%s/locations/global/recommenders/%s/recommendations' % (
            self.base_url,
            resource,
            recommender,
        )
        return self.requests.get(url).json().get('recommendations', [])
