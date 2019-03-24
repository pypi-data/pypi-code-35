"""BITS AWS Account class file."""

import boto3
import json
import re


class Account(object):
    """BITS AWS Account class."""

    def __init__(self):
        """Initialize an AWS Account instance."""
        self.aws = None
        self.google = None
        self.verbose = False

        # basic aws account attributes
        self.arn = None
        self.email = None
        self.id = None
        self.joined_method = None
        self.joined_timestamp = None
        self.name = None
        self.status = None
        self.suspended = False

        # aws organization (parent)
        self.organization_id = None

        # additional account attributes
        self.alias = None
        self.details = None
        self.summary = None

        # additional aws data
        self.groups = []
        self.policies = []
        self.roles = []
        self.users = []

        # bitsdb data
        self.admins = []
        # self.approvers = []
        # self.saml_users = []
        # self.owners = []

        # bitsdb budget data
        self.budget_start = None
        self.budget_end = None
        self.cost_object = None
        self.monthly_budget = None
        self.total_budget = None

        # authentication credentials
        self.credentials = None

        # clients
        self.s3_client = None
        self.iam_client = None
        self.sts_client = None

        # resources
        self.iam = None

        # admin managed policy
        self.admin_arn = 'arn:aws:iam::aws:policy/AdministratorAccess'
        self.admin_policy = {
            'PolicyName': 'AdministratorAccess',
            'PolicyArn': self.admin_arn,
        }

        # billing managed policy
        self.billing_arn = 'arn:aws:iam::aws:policy/job-function/Billing'
        self.billing_policy = {
            'PolicyName': 'Billing',
            'PolicyArn': self.billing_arn,
        }

        # default password policy
        self.default_password_policy = {
            "AllowUsersToChangePassword": True,
            "ExpirePasswords": False,
            "HardExpiry": False,
            # "MaxPasswordAge": 0,
            "MinimumPasswordLength": 8,
            "PasswordReusePrevention": 5,
            "RequireLowercaseCharacters": True,
            "RequireNumbers": True,
            "RequireSymbols": False,
            "RequireUppercaseCharacters": True,
        }

        # google idp xml
        self.google_xml = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<md:EntityDescriptor xmlns:md="urn:oasis:names:tc:SAML:2.0:metadata" entityID="https://accounts.google.com/o/saml2?idpid=C00q9u7iu" validUntil="2021-12-13T21:44:23.000Z">
<md:IDPSSODescriptor WantAuthnRequestsSigned="false" protocolSupportEnumeration="urn:oasis:names:tc:SAML:2.0:protocol">
    <md:KeyDescriptor use="signing">
    <ds:KeyInfo xmlns:ds="http://www.w3.org/2000/09/xmldsig#">
        <ds:X509Data>
        <ds:X509Certificate>MIIDdDCCAlygAwIBAgIGAWlAEDbpMA0GCSqGSIb3DQEBCwUAMHsxFDASBgNVBAoTC0dvb2dsZSBJ
bmMuMRYwFAYDVQQHEw1Nb3VudGFpbiBWaWV3MQ8wDQYDVQQDEwZHb29nbGUxGDAWBgNVBAsTD0dv
b2dsZSBGb3IgV29yazELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWEwHhcNMTkwMzAy
MjAxOTU3WhcNMjQwMjI5MjAxOTU3WjB7MRQwEgYDVQQKEwtHb29nbGUgSW5jLjEWMBQGA1UEBxMN
TW91bnRhaW4gVmlldzEPMA0GA1UEAxMGR29vZ2xlMRgwFgYDVQQLEw9Hb29nbGUgRm9yIFdvcmsx
CzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpDYWxpZm9ybmlhMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8A
MIIBCgKCAQEArpI3FCDzKjB/P8+0LRgo5icgVeSFO2cQ40X6CfTSBz/7snlS/MM51EWFGEAhbUkn
fm5bfKORKql823XXdreTXnu3OmWlGd7I9gFE3O0zeiaUBubrG/Re5I/+eZj8Cd0tZ2PQ+zpQ1hEd
Vdbf/2NIe8A8r3QHB53Suf0a4/4n+HBiUO6UiZ+is3tXyPBFpiTjI8z41oYCJigvy7Xyf36Lstju
ibZPwZxbhncaPLEPPj9kqTYUiCKpKwSZUDISpaNXYnf/prHEkFSxQdkGev4I6ygilAb7RVtF8Ghf
2kPcmjnlWL8ea7aNf4WehR9ZnvK4Ib7MWLNrvB5WBxxwJrXXXwIDAQABMA0GCSqGSIb3DQEBCwUA
A4IBAQB8bLu4bgnnEBqIM06JtJSQ5pDslFc9un2/zcXr0AHgrFTV/DtpvSlARQFco30UJ4cua4b5
O4bdef6yBBRDAZfSrY8lhwbcrydN13fWk2ni30DPbthYDTuVD0Ufvm6sIbY58Oc0Zh9jn5svOCeC
6wdBCF0QkGxh6lXRHyoI2GeJXI5F2LJGG2bT+hFhJjbY66A4Y/BR3MqYF3NUfl02ddBJL+jNblf3
zCBAf8nK0dJKGM1u1EBe7IHvCE32MoDoGzxFx+mLbcm1vBRuz839GYFpFCWQufF085B/wzVLrSF/
ptQk1EkL5BGPzllq6WNuw9Pg3d8xAhFE1sd2LPw3TRs5</ds:X509Certificate>
        </ds:X509Data>
    </ds:KeyInfo>
    </md:KeyDescriptor>
    <md:NameIDFormat>urn:oasis:names:tc:SAML:1.1:nameid-format:emailAddress</md:NameIDFormat>
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect" Location="https://accounts.google.com/o/saml2/idp?idpid=C00q9u7iu"/>
    <md:SingleSignOnService Binding="urn:oasis:names:tc:SAML:2.0:bindings:HTTP-POST" Location="https://accounts.google.com/o/saml2/idp?idpid=C00q9u7iu"/>
</md:IDPSSODescriptor>
</md:EntityDescriptor>"""

    def __repr__(self):
        """Return a human-reable representation of the instance."""
        account = '<AWS Account - %s: %s [%s]>' % (
            self.id,
            self.name,
            self.alias,
        )
        return account

    #
    # Create from an AWS Account record
    #
    def from_aws(
        self,
        aws,
        account,
        include_alias=False,
        include_details=False,
        include_summary=False,
    ):
        """Return an account based off AWS data."""
        self.aws = aws
        self.verbose = aws.verbose

        # set account details
        self.arn = account.get('Arn')
        self.email = account.get('Email')
        self.id = account.get('Id')
        self.joined_method = account.get('JoinedMethod')
        self.joined_timestamp = account.get('JoinedTimestamp')
        self.name = account.get('Name')
        self.status = account.get('Status')

        # set organization_id (parent)
        if self.id != self.aws.root_account:
            self.organization_id = self.aws.root_account

        # check status
        if self.status == 'SUSPENDED':
            self.suspended = True
            return self

        # get account credentials
        self.get_credentials()

        # get account alias from aws
        if include_alias:
            self.refresh_alias()

        # get account details
        if include_details:
            self.refresh_details()

        # get account summary
        if include_summary:
            self.refresh_summary()

        return self

    def from_bitsdb(
        self,
        aws,
        account,
        include_details=False,
        include_summary=False,
    ):
        """Return an account based off a BITSdb record."""
        self.aws = aws
        self.verbose = aws.verbose

        # set account details
        self.arn = account.get('arn')
        self.admins = account.get('admins')
        self.alias = account.get('alias')
        self.email = account.get('email')
        self.id = account.get('id')
        # self.joined_method = account.get('joined_method')
        # self.joined_timestamp = account.get('joined_timestamp')
        self.organization_id = account.get('organization_id')
        self.name = account.get('name')
        self.status = account.get('status')

        # set organization_id (parent)
        if self.id != self.aws.root_account:
            self.organization_id = self.aws.root_account

        # check status
        if self.status == 'SUSPENDED':
            self.suspended = True
            return self

        # get account credentials
        self.get_credentials()

        # get account details
        if include_details:
            self.refresh_details()

        # get account summary
        if include_summary:
            self.refresh_summary()

        return self

    def from_create_account_status(
        self,
        aws,
        status,
        alias=None,
        email=None,
        include_details=False,
        include_summary=False,
    ):
        """Return an account based off of "CreateAccountStatus"."""
        self.aws = aws
        self.verbose = aws.verbose

        # set account details from arguments
        self.alias = alias
        self.email = email

        # set account details from status
        self.id = status.get('AccountId')
        self.name = status.get('AccountName')

        # get account credentials
        self.get_credentials()

        # get account details
        if include_details:
            self.refresh_details()

        # get account summary
        if include_summary:
            self.refresh_summary()

        return self

    #
    # Output record for BITSdb API
    #
    def to_bitsdb(self):
        """Return a BITSDB AwsAccount record."""
        account = {
            'kind': 'aws#account',
            'id': self.id,
            'account_id': self.id,
            'alias': self.alias,
            'arn': self.arn,
            'email': self.email,
            'name': self.name,
            'organization_id': self.organization_id,
            'status': self.status,
            'admins': self.admins,
        }
        return account

    #
    # Account ID
    #
    def get_account_id(self):
        """Return the email address for the account."""
        return self.get_caller_identity().get('Account')

    #
    # Caller Identity
    #
    def get_caller_identity(self):
        """Return the identity of the caller."""
        return self.sts_client.get_caller_identity()

    #
    # Credentials
    #
    def get_credentials(self):
        """Return credentials for this account."""
        role_name = 'role/OrganizationAccountAccessRole'
        role = 'arn:aws:iam::%s:%s' % (
            self.id,
            role_name,
        )
        self.credentials = self.aws.assume_role(role, 'iam')

        self.iam_client = boto3.client(
            'iam',
            aws_access_key_id=self.credentials['AccessKeyId'],
            aws_secret_access_key=self.credentials['SecretAccessKey'],
            aws_session_token=self.credentials['SessionToken'],
        )

        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.credentials['AccessKeyId'],
            aws_secret_access_key=self.credentials['SecretAccessKey'],
            aws_session_token=self.credentials['SessionToken'],
        )

        self.sts_client = boto3.client(
            'sts',
            aws_access_key_id=self.credentials['AccessKeyId'],
            aws_secret_access_key=self.credentials['SecretAccessKey'],
            aws_session_token=self.credentials['SessionToken'],
        )

        # create resources
        self.iam = boto3.resource(
            'iam',
            aws_access_key_id=self.credentials['AccessKeyId'],
            aws_secret_access_key=self.credentials['SecretAccessKey'],
            aws_session_token=self.credentials['SessionToken'],
        )

        return self.credentials

    #
    # Account Authorization Details
    #
    def get_details(self):
        """Return details for this account."""
        # get auth details
        details = self.iam_client.get_account_authorization_details(
            MaxItems=1000
        )

        # retrieve additional pages of details
        while details['IsTruncated']:

            # get next page of results
            more = self.iam_client.get_account_authorization_details(
                Marker=details['Marker'],
                MaxItems=1000,
            )

            # merge lists
            for key in sorted(more):
                if key in [
                        'GroupDetailList',
                        'Policies',
                        'RoleDetailList',
                        'UserDetailList',
                ]:
                    more[key] += details[key]

            details = more

        return details

    def refresh_alias(self):
        """Refresh alias from AWS."""
        self.alias = self.get_alias()

    def refresh_details(self):
        """Refresh account details from AWS."""
        self.details = self.get_details()
        self.groups = self.details['GroupDetailList']
        self.policies = self.details['Policies']
        self.roles = self.details['RoleDetailList']
        self.users = self.details['UserDetailList']

    def refresh_summary(self):
        """Refresh the account summary from AWS."""
        self.summary = self.get_summary()

    #
    # Account Summary
    #
    def get_summary(self):
        """Return the summary information for this account."""
        summary = self.iam.AccountSummary()
        return summary.summary_map

    #
    # Access Keys
    #
    def delete_access_key(self, user_name, key_id):
        """Delete an access key."""
        self.iam_client.delete_access_key(
            UserName=user_name,
            AccessKeyId=key_id,
        )

    def list_access_keys(self, user_name):
        """List access keys."""
        return self.iam_client.list_access_keys(
            UserName=user_name
        )

    #
    # Account Alias
    #
    def create_alias(self, alias):
        """Create account alias."""
        return self.iam_client.create_account_alias(
            AccountAlias=alias,
        )

    def delete_alias(self, alias):
        """Delete account alias."""
        return self.iam_client.delete_account_alias(
            AccountAlias=alias,
        )

    def get_alias(self):
        """Return the alias for this account."""
        aliases = self.list_aliases()
        if aliases:
            return aliases[0]

    def list_aliases(self):
        """Return the alias for this account."""
        return self.iam_client.list_account_aliases().get('AccountAliases', [])

    #
    # Account Password Policy
    #
    def get_account_password_policy(self):
        """Return the password policy for this account."""
        try:
            response = self.iam_client.get_account_password_policy()
            return response.get('PasswordPolicy')
        except Exception:
            return

    def update_account_password_policy(self, policy):
        """Update the password policy for this account."""
        return self.iam_client.update_account_password_policy(**policy)

    #
    # Buckets
    #
    def list_buckets(self):
        """Return a list of buckets."""
        return self.s3_client.list_buckets().get('Buckets', [])

    #
    # Groups
    #
    def create_group(self, groupname):
        """Create a group."""
        return self.iam_client.create_group(
            GroupName=groupname,
        )

    def list_groups(self):
        """Return a list of groups."""
        return self.iam_client.get_groups().get('Groups', [])

    #
    # Group Policies
    #
    def attach_group_policy(self, groupname, arn):
        """Attach a group policy."""
        return self.iam_client.attach_group_policy(
            GroupName=groupname,
            PolicyArn=arn,
        )

    def detach_group_policy(self, groupname, arn):
        """Attach a group policy."""
        return self.iam_client.detach_group_policy(
            GroupName=groupname,
            PolicyArn=arn,
        )

    #
    # Policies
    #
    def delete_policy(self, arn):
        """Delete a policy."""
        return self.iam_client.delete_policy(
            PolicyArn=arn
        )

    def list_policies(self):
        """Return a list of policies."""
        return self.iam_client.list_policies(
            Scope='Local'
        ).get('Policies', [])

    #
    # Policy Versions
    #
    def create_policy_version(self, arn, document):
        """Create a policy version."""
        return self.iam_client.create_policy_version(
            PolicyArn=arn,
            PolicyDocument=document,
            SetAsDefault=True,
        )

    def list_policy_version(self, arn, document):
        """List policy versions."""
        return self.iam_client.list_policy_versions(
            PolicyArn=arn,
        )

    def delete_policy_version(self, arn, version):
        """Delete a policy version."""
        return self.iam_client.create_policy_version(
            PolicyArn=arn,
            VersionId=version,
        )

    #
    # Role Policies
    #
    def attach_role_policy(self, role_name, arn):
        """Attach a role policy."""
        return self.iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=arn,
        )

    def detach_role_policy(self, role_name, arn):
        """Detach a role policy."""
        return self.iam_client.detach_role_policy(
            RoleName=role_name,
            PolicyArn=arn,
        )

    def list_attached_role_policies(self, role_name):
        """List role policies."""
        return self.iam_client.list_attached_role_policies(
            RoleName=role_name,
        ).get('AttachedPolicies', [])

    #
    # Roles
    #
    def create_role(self, role_name, policy):
        """Create a role."""
        return self.iam_client.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=policy,
        )

    def delete_role(self, role_name):
        """Delete a role."""
        return self.iam_client.delete_role(
            RoleName=role_name,
        )

    def list_roles(self):
        """Return a list of roles."""
        return self.iam_client.list_roles().get('Roles', [])

    #
    # SAML Providers
    #
    def create_saml_provider(self, name, metadata):
        """Create SAML provider."""
        return self.iam_client.create_saml_provider(
            Name=name,
            SAMLMetadataDocument=metadata,
        )

    def get_saml_provider(self, arn):
        """Return a list of SAML providers."""
        return self.iam_client.get_saml_provider(SAMLProviderArn=arn)

    def list_saml_providers(self):
        """Return a list of SAML providers."""
        return self.iam_client.list_saml_providers().get('SAMLProviderList', [])

    def saml_metadata_document(self, arn):
        """Return the SAML metadata document."""
        self.iam.SamlProvider(arn).saml_metadata_document

    def update_saml_provider(self, arn):
        """Return the SAML metadata document."""
        return self.iam_client.update_saml_provider(
            SAMLMetadataDocument=self.google_xml,
            SAMLProviderArn=arn
        )

    #
    # User Policies
    #
    def detach_user_policy(self, username, arn):
        """Detach a user policy."""
        return self.iam_client.detach_user_policy(
            UserName=username,
            PolicyArn=arn,
        )

    def put_user_policy(self, username, policy, document):
        """Put a user policy."""
        return self.iam_client.put_user_policy(
            UserName=username,
            PolicyName=policy,
            PolicyDocument=document,
        )

    #
    # Users
    #
    def create_user(self, user_name):
        """Create a user."""
        return self.iam_client.create_user(
            UserName=user_name,
        )

    def delete_user(self, user_name):
        """Delete a user."""
        return self.iam_client.delete_user(
            UserName=user_name,
        )

    def list_users(self):
        """Return a list of users."""
        return self.iam_client.list_users().get('Users', [])

    #
    # Display Functions
    #
    def display(self):
        """Display information about this account."""
        print('%s: %s [%s] - %s' % (
            self.alias,
            self.name,
            self.id,
            self.status
        ))
        if self.status == 'SUSPENDED':
            return

        self.display_groups()
        self.display_policies()
        self.display_roles()
        self.display_users()

    def display_groups(self):
        """Display groups."""
        if self.groups:
            print('  * Groups: %s' % (len(self.groups)))
        if self.verbose:
            for group in sorted(self.groups, key=lambda x: x['GroupName']):
                print('      * %s' % (group['GroupName']))

    def display_policies(self):
        """Display policies."""
        if self.policies:
            print('  * Policies: %s' % (len(self.policies)))
        if self.verbose:
            for policy in sorted(self.policies, key=lambda x: x['PolicyName']):
                print('      * %s' % (policy['PolicyName']))

    def display_roles(self):
        """Display roles."""
        if self.roles:
            print('  * Roles: %s' % (len(self.roles)))
        if self.verbose:
            for role in sorted(self.roles, key=lambda x: x['RoleName']):
                print('      * %s' % (role['RoleName']))

    def display_users(self):
        """Display users."""
        if self.users:
            print('  * Users: %s' % (len(self.users)))
        if self.verbose:
            for user in sorted(self.users, key=lambda x: x['UserName']):
                print('      * %s' % (user['UserName']))

    #
    # Updates
    #
    def update(self):
        """Update this account."""
        # update account alias
        self.update_alias(self.alias)

        # get account details
        self.refresh_details()

        # update groups
        self.update_groups()

        # update account role
        self.update_roles()

        # update users
        self.update_users()

        # update password policy
        self.update_password_policy()

        # update saml provider
        self.update_google_saml_provider()

    def update_alias(self, alias):
        """Update account alias."""
        self.refresh_alias()

        # if alias doesn't exist, create it
        if alias and not self.alias:
            self.create_alias(alias)
            print('    + Created alias: %s' % (alias))

        # if alias is incorrect, update it
        elif alias != self.alias:
            self.delete_alias(self.alias)
            self.create_alias(alias)
            print('    * Updated alias from %s to %s' % (self.alias, alias))
            self.alias = alias

    #
    # Update Groups
    #
    def check_group(self, group_name):
        """Check a group to see if it exists in account details."""
        # return None if no groups list
        if not self.groups:
            return

        # check groups
        for group in self.groups:
            if group_name == group['GroupName']:
                return group

    def check_group_managed_policies(self, group_name):
        """Check a group's managed policies."""
        # find the given group in the group detail list
        group = self.check_group(group_name)

        # if no group, return
        if not group:
            print('    * ERROR: No such group: %s' % (group_name))
            return

        # get policies
        policies = group['AttachedManagedPolicies']

        # check if admin managed policy exists
        if group_name in ['Admins']:
            if self.admin_policy not in policies:
                # attach admin policy
                self.attach_group_policy(group_name, self.admin_arn)
                if self.verbose:
                    print('      + Added admin policy to group: %s' % (
                        group_name,
                    ))

        # check if billing managed policy exists
        if group_name in ['Admins', 'BillingAdmins']:
            if self.billing_policy not in policies:
                # attach billing policy
                self.attach_group_policy(group_name, self.billing_arn)
                if self.verbose:
                    print('      + Added billing policy to role: %s' % (
                        group_name,
                    ))

        # make sure billing admins doesn't have the admin policy
        if group_name in ['BillingAdmins']:
            if self.admin_policy in policies:
                # detach admin policy
                self.detach_group_policy(group_name, self.admin_arn)
                if self.verbose:
                    print('      - Removed admin policy from role: %s' % (
                        group_name,
                    ))

    def update_group(self, group_name, policy_name):
        """Update a single group."""
        created = False

        # check if group exists
        group_check = self.check_group(group_name)
        if group_check:
            if self.verbose:
                print('    * Group exists: %s' % (group_name))

        # if not, create it
        else:
            # create the IAM group
            result = self.create_group(group_name)
            if 'Group' in result:
                print('    + Created group: %s' % (group_name))
                created = True

        # if we created a role, let's update the account details
        if created:
            self.refresh_details()

        # check role policies
        self.check_group_managed_policies(group_name)

    def update_groups(self):
        """Update groups for an account."""
        # update the admins group
        self.update_group('Admins', 'AdministratorAccess')
        # update the billing group
        self.update_group('BillingAdmins', 'Billing')

    #
    # Update Pasword Policy
    #
    def update_password_policy(self):
        """Update the account password policy."""
        policy = self.get_account_password_policy()
        newpolicy = self.default_password_policy.copy()

        # if policy doesn't exist, create it
        if not policy:
            del newpolicy['ExpirePasswords']
            self.update_account_password_policy(newpolicy)
            print('    + Created password policy')
            return

        # check if policy needs to be updated
        updates = []
        for key in sorted(set(list(policy) + list(newpolicy))):
            o = policy.get(key)
            n = newpolicy.get(key)
            if o != n:
                updates.append('%s: %s -> %s' % (
                    key,
                    json.dumps(o),
                    json.dumps(n)
                ))
        if updates:
            if self.verbose:
                print('    * Updating password policy:')
                print('      * '+'\n      * '.join(updates))
            del newpolicy['ExpirePasswords']
            self.update_account_password_policy(newpolicy)
            print('    * Updated password policy')

    #
    # Update Roles
    #
    def check_role(self, role_name):
        """Check a role to see if it exists in account details."""
        # return None if no roles list
        if not self.roles:
            return

        # check roles
        for role in self.roles:
            if role_name == role['RoleName']:
                return role

    def check_role_managed_policies(self, role_name):
        """Check the policy for a specific role."""
        # find the given role in the role detail list
        role = self.check_role(role_name)

        # if no role, return
        if not role:
            print('    * ERROR: No such role: %s' % (role_name))
            return

        # get policies
        policies = role['AttachedManagedPolicies']

        # check if admin managed policy exists
        if self.admin_policy not in policies:
            # attach admin policy
            self.attach_role_policy(role_name, self.admin_arn)
            if self.verbose:
                print('      + Added admin policy to role: %s' % (
                    role_name,
                ))

        # check if billing managed policy exists
        if self.billing_policy not in policies:
            # attach billing policy
            self.attach_role_policy(role_name, self.billing_arn)
            if self.verbose:
                print('      + Added billing policy to role: %s' % (
                    role_name,
                ))

    def generate_google_role_policy(self):
        """Return the google role policy."""
        google_role_name = 'saml-provider/google-idp'
        arn = 'arn:aws:iam::%s:%s' % (self.id, google_role_name)
        role = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "Federated": arn
                    },
                    "Action": "sts:AssumeRoleWithSAML",
                    "Condition": {
                        "StringEquals": {
                            "SAML:aud": "https://signin.aws.amazon.com/saml"
                        }
                    }
                }
            ]
        }
        return json.dumps(role)

    def generate_org_role_policy(self):
        """Return the org role policy."""
        role = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "arn:aws:iam::%s:root" % (
                            self.aws.root_account
                        ),
                    },
                    "Action": "sts:AssumeRole",
                }
            ]
        }
        return json.dumps(role)

    def update_role(self, role_name, policy):
        """Update a single role."""
        created = False

        # check if role exists
        role_check = self.check_role(role_name)
        if role_check:
            if self.verbose:
                print('    * Role exists: %s' % (role_name))

        # if not, create it
        else:
            """CREATE THE IAM ROLE."""
            result = self.create_role(role_name, policy)
            if 'Role' in result:
                print('    + Created role: %s' % (role_name))
                created = True

        # if we created a role, let's update the account details
        if created:
            self.refresh_details()

        # check role policies
        self.check_role_managed_policies(role_name)

    def update_roles(self):
        """Update account roles."""
        # update org role
        self.update_role(
            'OrganizationAccountAccessRole',
            self.generate_org_role_policy(),
        )

        # update google admin role
        self.update_role(
            'google-admin-role',
            self.generate_google_role_policy(),
        )

        # delete roles
        delete = [
            'bitsdb-role',
        ]
        for role_name in sorted(delete):
            if self.check_role(role_name):
                policies = self.list_attached_role_policies(role_name)
                for p in sorted(policies, key=lambda x: x['PolicyName']):
                    # detach the policy
                    self.detach_role_policy(role_name, p['PolicyArn'])
                    print('    * Detached policy from role %s: %s' % (
                        role_name,
                        p['PolicyName'],
                    ))
                # delete the role
                self.delete_role(role_name)
                print('    * Deleted role: %s' % (role_name))

    #
    # Update SAML Provider
    #
    def check_saml_provider(self):
        """Return the google-idp saml provider if it exists."""
        saml_providers = self.list_saml_providers()
        google_idp = '%s:saml-provider/google-idp' % (self.id)

        for provider in saml_providers:
            arn = provider['Arn']
            if re.search('%s$' % (google_idp), arn):
                return provider

    def check_saml_provider_cert(self, saml_check):
        """Return the cert for the SAML provider."""
        arn = saml_check['Arn']
        saml_provider = self.get_saml_provider(arn)
        metadata_document = saml_provider['SAMLMetadataDocument']
        if metadata_document != self.google_xml:
            self.update_saml_provider(arn)
            return arn

    def update_google_saml_provider(self):
        """Update the SAML profider for an account."""
        saml_check = self.check_saml_provider()

        # create the google IDP to allow G-Suite logins to the account
        if not saml_check:
            result = self.create_saml_provider('google-idp', self.google_xml)
            if 'SAMLProviderArn' in result:
                arn = result['SAMLProviderArn']
                print('    * Created SAML provider: %s' % (arn))

        # check the saml certificate
        saml_cert_check = self.check_saml_provider_cert(saml_check)

        # check if the cert needed to be updated
        if saml_cert_check:
            print('    * Updated SAML provider certificate: %s' % (saml_cert_check))

    #
    # Update Users
    #
    def check_user(self, user_name):
        """Check if a user exists."""
        # return None if no users list
        if not self.users:
            return

        # check users
        for user in self.users:
            if user_name == user['UserName']:
                return user

    def update_users(self):
        """Update account roles."""
        # delete users that should not exist
        delete = [
            'cloudlock',
        ]
        for user_name in sorted(delete):
            if self.check_user(user_name):
                self.delete_user(user_name)
                print('    * Deleted user: %s' % (user_name))
