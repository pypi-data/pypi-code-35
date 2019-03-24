"""BITS AWS class file."""

import boto3
import os
import time

from bits.aws.account import Account


class AWS(object):
    """BITS AWS class."""

    def __init__(
        self,
        auth=None,
        aws_access_key_id=None,
        aws_secret_access_key=None,
        credentials_file='credentials',
        root_account=None,
        verbose=False
    ):
        """Initialize a class instance."""
        self.auth = auth
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.credentials_file = credentials_file
        self.root_account = root_account
        self.verbose = verbose

        # set environment variable
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = credentials_file

        # check credentials
        params = {}
        if aws_access_key_id and aws_secret_access_key:
            params['aws_access_key_id'] = aws_access_key_id
            params['aws_secret_access_key'] = aws_secret_access_key

        # create resources
        self.iam = boto3.resource('iam', **params)
        self.s3 = boto3.resource('s3', **params)

        # create clients
        self.iam_client = boto3.client('iam', **params)
        self.organizations_client = boto3.client('organizations', **params)
        self.s3_client = boto3.client('s3', **params)
        self.sts_client = boto3.client('sts', **params)

        # classes
        self.account = Account

        # data
        self.accounts = None
        self.permissions = None

        # account creation parameters
        self.flags = None

    def assume_role(self, role_name, resource):
        """Return credentials for an assumed role."""
        assumedRoleObject = self.sts_client.assume_role(
            RoleArn=role_name,
            RoleSessionName="AssumeRoleSession1"
        )
        credentials = assumedRoleObject['Credentials']
        return credentials

    def create_organization_account(self, email, name):
        """Create a new account in the organization."""
        params = {
            'AccountName': name,
            'Email': email,
            'IamUserAccessToBilling': 'ALLOW',
            # 'RoleName': 'OrganizationAccountAccessRole',
        }

        # example_response = {
        #     'CreateAccountStatus': {
        #         'Id': 'string',
        #         'AccountName': 'string',
        #         'State': 'IN_PROGRESS'|'SUCCEEDED'|'FAILED',
        #         'RequestedTimestamp': datetime(2015, 1, 1),
        #         'CompletedTimestamp': datetime(2015, 1, 1),
        #         'AccountId': 'string',
        #         'FailureReason': 'ACCOUNT_LIMIT_EXCEEDED'|'EMAIL_ALREADY_EXISTS'|'INVALID_ADDRESS'|'INVALID_EMAIL'|'CONCURRENT_ACCOUNT_MODIFICATION'|'INTERNAL_FAILURE'
        #     }
        # }

        response = self.organizations_client.create_account(**params)

        while response and 'CreateAccountStatus' in response:
            # get status from response
            status = response['CreateAccountStatus']

            # check failure reason
            failure_reason = status.get('FailureReason')
            if failure_reason:
                print('ERROR: Account Creation failed: %s!' % (failure_reason))
                return

            # look for account id
            if 'AccountId' in status:
                return status

            # check operation
            operation_id = status.get('Id')

            # sleep 1 before hitting the api again
            time.sleep(1)

            # check the operation
            response = self.organizations_client.describe_create_account_status(
                CreateAccountRequestId=operation_id,
            )

    def get_accounts(
        self,
        include_alias=True,
        include_details=False,
        include_summary=False
    ):
        """Return a list of account objects."""
        accounts_list = self.get_organization_accounts()
        accounts = []
        for aws_account in accounts_list:
            account = self.account().from_aws(
                self,
                aws_account,
                include_alias=True,
                include_details=include_details,
                include_summary=include_summary
            )
            accounts.append(account)
        return(accounts)

    def get_accounts_dict(self):
        """Return a dict of accounts from AWS."""
        accounts_list = self.get_accounts()
        accounts = {}
        for a in accounts_list:
            accounts[a.id] = a
        return(accounts)

    def get_organization_accounts(self):
        """Return a list of accounts from AWS."""
        client = self.organizations_client

        response = client.list_accounts()
        accounts = response.get('Accounts', [])
        next_token = response.get('NextToken')

        while next_token:
            response = client.list_accounts(NextToken=next_token)
            next_token = response.get('NextToken')
            accounts += response.get('Accounts', [])

        return accounts
