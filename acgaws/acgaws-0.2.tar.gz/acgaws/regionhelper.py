"""
AWS Region helper module
"""
import boto3
from awsretry import AWSRetry


class RegionHelper(object):

    def __init__(self):
        self.client = boto3.Session()

    @AWSRetry.backoff()
    def get_regions(self, service):
        """Get the available regions for a service

        Args:
            service:

        Returns:

        """
        """Get the available regions for a specific service

        :param service: the AWS service to list available regions (ec2, rds, etc)
        :return: List of available regions
        """

        available_regions = self.client.get_available_regions(service)
        return available_regions
