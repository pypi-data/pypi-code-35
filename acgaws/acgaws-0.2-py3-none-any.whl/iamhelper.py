"""
AWS IAM helper module
"""
import boto3
from awsretry import AWSRetry
from datetime import datetime, timezone


class IamHelper(object):

    def __init__(self):
        self.client = boto3.client('iam')

    @AWSRetry.backoff()
    def get_all_users(self):
        """Get a list of all the users in IAM

        Returns:
            A list of all IAM user in AWS

        """
        all_users = []
        user_list = self.client.list_users()
        marker = user_list.get('Marker', None)
        all_users += [user['UserName'] for user in user_list['Users']]
        while marker:
            user_list = self.client.list_users(Marker=marker)
            marker = user_list.get('Marker', None)
            all_users += [user['UserName'] for user in user_list['Users']]

        return all_users

    @AWSRetry.backoff()
    def get_last_console_access(self, username):
        """Gets the last time a user accessed the console

        Args:
            username: User to look up

        Returns:
            The number of days since the user last used the console
            or -1 if they have never used it.

        """
        user = self.client.get_user(UserName=username)
        if 'PasswordLastUsed' in user['User']:
            console_last_login_date = datetime.now(timezone.utc) - user['User']['PasswordLastUsed']
            console_last_login_age = console_last_login_date.days
        else:
            console_last_login_age = -1

        return console_last_login_age

    @AWSRetry.backoff()
    def get_api_access_keys(self, username):
        """Gets a list of the access keys the user has created

        Args:
            username: User to lookup

        Returns:
            A list of API keys

        """
        api_access_keys = []
        access_key_list = self.client.list_access_keys(UserName=username)
        for access_key in access_key_list['AccessKeyMetadata']:
            api_access_keys.append(access_key['AccessKeyId'])

        return api_access_keys

    @AWSRetry.backoff()
    def delete_api_access_keys(self, username):
        access_key_list = self.get_api_access_keys(username)
        for access_key in access_key_list:
            self.client.delete_access_key(UserName=username, AccessKeyId=access_key)

        return 0

    @AWSRetry.backoff()
    def get_last_api_access(self, access_key_list):
        """Gets the last time a user accessed the API

        Args:
            access_key_list: List of Access Key to Lookup

        Returns:
            The number of days since the user last used the API
            or -1 if they have never used it.

        """
        api_key_ages = []
        for access_key in access_key_list:
            last_used = self.client.get_access_key_last_used(AccessKeyId=access_key)
            for key, value in last_used['AccessKeyLastUsed'].items():
                if key == "LastUsedDate":
                    api_aged_date = datetime.now(timezone.utc) - value
                    api_key_ages.append(api_aged_date.days)
        if not api_key_ages:
            api_key_ages.append(-1)

        return min(api_key_ages)

    @AWSRetry.backoff()
    def disable_console_access(self, username):
        """Disable Console Access

        Args:
            username: User to disable

        Returns:
            Return code

        """
        return self.client.delete_login_profile(UserName=username)

    @AWSRetry.backoff()
    def disable_api_access(self, username, access_key):
        """Disable API Access

        Args:
            username: Username to disable
            access_key: Access key to disable

        Returns:
            Return Code

        """

        return self.client.update_access_key(UserName=username, AccessKeyId=access_key, Status='Inactive')

    @AWSRetry.backoff()
    def get_user_tags(self, username):
        tag_values = {}
        tags = self.client.list_user_tags(UserName=username)
        for tag in tags['Tags']:
            tag_values[tag["Key"]] = tag["Value"]

        return tag_values

    @AWSRetry.backoff()
    def tag_deletion_date(self, username, date):
        """Tag the IAM resource with a Deletion Date

        Args:
            username: User to tag
            date: Date to use for tag

        Returns:
            Return Code

        """

        return self.client.tag_user(UserName=username, Tags=[{'Key': 'DeleteDate', 'Value': date}])

    @AWSRetry.backoff()
    def delete_user(self, username):
        """Delete a User from IAM

        Args:
            username: User to Delete

        Returns:
            Return Code
        """

        return self.client.delete_user(UserName=username)

    @AWSRetry.backoff()
    def get_user_groups(self, username):
        """Get the groups a user is in

        Args:
            username: User to get groups of

        Returns:
            List of groups

        """
        user_groups = []
        list_of_groups = self.client.list_groups_for_user(UserName=username)
        for group in list_of_groups['Groups']:
            user_groups.append(group["GroupName"])

        return user_groups

    @AWSRetry.backoff()
    def remove_user_from_group(self, username):
        """Remove a user from a group

        Args:
            username: Username to remove from group

        Returns:
            Return code

        """
        groups = self.get_user_groups(username)
        for group in groups:
            self.client.remove_user_from_group(UserName=username, GroupName=group)

        return 0

    @AWSRetry.backoff()
    def list_attached_user_policies(self, username):
        """List the User Policies

        Args:
            username: User to get policies

        Returns:
            A list of policy arns to be removed

        """
        user_policies = []
        user_policy_list = self.client.list_attached_user_policies(UserName=username)
        for policy in user_policy_list['AttachedPolicies']:
            user_policies.append(policy['PolicyArn'])

        return user_policies

    @AWSRetry.backoff()
    def detach_user_policies(self, username):
        """Detaches user policies

        Args:
            username:
            policy_arn:

        Returns:

        """
        policy_arns = self.list_attached_user_policies(username)
        for arn in policy_arns:
            self.client.detach_user_policy(UserName=username, PolicyArn=arn)

        return 0

    @AWSRetry.backoff()
    def list_mfa(self,username):
        mfa_devices = []
        all_mfa_devices = self.client.list_mfa_devices(UserName=username)
        for mfa in all_mfa_devices['MFADevices']:
            mfa_devices.append(mfa['SerialNumber'])

        return mfa_devices

    @AWSRetry.backoff()
    def deactivate_mfa(self, username):
        mfa_serials = self.list_mfa(username)
        for serial in mfa_serials:
            self.client.deactivate_mfa_device(UserName=username, SerialNumber=serial)

        return 0



