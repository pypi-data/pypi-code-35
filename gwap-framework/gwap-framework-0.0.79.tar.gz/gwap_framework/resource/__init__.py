from gwap_framework.resource.base import BaseResource


class HealthCheckResource(BaseResource):

    def get(self):
        return {
            'status': 'Healthy'
        }
