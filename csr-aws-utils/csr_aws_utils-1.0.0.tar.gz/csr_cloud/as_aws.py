import boto3
import datetime
import logging
import ast
import os
from botocore.client import Config
from collections import namedtuple
import re
import string
import json

logger = logging.getLogger('autoscaler')

def createRandomPassword(pwdLength=15, specialChars="False"):
    logger.info("Creating random password")
    if specialChars is None:
        specialChars = "True"
    # Generate new random password
    chars = string.ascii_letters + string.digits
    if specialChars == "True":
        chars += '#$%^&+='
        p = re.compile(
            '^(?=.{1,})(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[#$%^&+=]).*$')
    else:
        p = re.compile('^(?=.{1,})(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).*$')
    numTries = 0
    pwdFound = False
    while not pwdFound:
        password = ''
        numTries += 1
        for i in range(int(pwdLength)):
            password += chars[ord(os.urandom(1)) % len(chars)]
        m = p.match(password)
        if m is not None:
            pwdFound = True
    logger.info("Password created after %s tries", numTries)
    logger.debug("%s", password)
    return password


def create_userdata(cfg, status, inst_num, fingerprint, autoscaler_tag):
    bgp_asn = status.get_bgp_asn()
    hostname = cfg.get_as_group_name() + '-' + str(inst_num)
    username = "automate"
    password = createRandomPassword()
    userdata = []
    userdata.append("license=\"%s\"\n" % cfg.get_license_level_type())

    userdata.append("ios-config-1=\"username %s priv 15 pass %s\n" %
                    (username, password))
    userdata.append("ios-config-2=\"service password-encryption\"\n")
    userdata.append("ios-config-3=\"crypto isakmp policy 200\"\n")
    userdata.append("ios-config-4=\"encryption aes 128\"\n")
    userdata.append("ios-config-5=\"authentication pre-share\"\n")
    userdata.append("ios-config-6=\"group 2\"\n")
    userdata.append("ios-config-7=\"lifetime 28800\"\n")
    userdata.append("ios-config-8=\"hash sha\"\n")
    userdata.append(
        "ios-config-9=\"crypto ipsec transform-set ipsec-prop-vpn-aws esp-aes 128 esp-sha-hmac\"\n")
    userdata.append("ios-config-10=\"mode tunnel\"\n")
    userdata.append("ios-config-11=\"crypto ipsec df-bit clear\"\n")

    userdata.append(
        "ios-config-12=\"crypto isakmp keepalive 10 10 on-demand\"\n")

    userdata.append(
        "ios-config-13=\"crypto ipsec security-association replay window-size 1024\"\n")
    userdata.append(
        "ios-config-14=\"crypto ipsec fragmentation before-encryption\"\n")
    userdata.append("ios-config-15=\"crypto ipsec profile ipsec-vpn-aws\"\n")
    userdata.append("ios-config-16=\"set pfs group2\"\n")
    userdata.append(
        "ios-config-17=\"set security-association lifetime seconds 3600\"\n")
    userdata.append("ios-config-18=\"set transform-set ipsec-prop-vpn-aws\"\n")

    userdata.append("ios-config-23=\"ip ssh pubkey-chain\"\n")
    userdata.append("ios-config-24=\"username %s %s" % (username, "\"\n"))

    userdata.append("ios-config-25=\"key-hash ssh-rsa %s %s" %
                    (fingerprint, "\"\n"))
    userdata.append(
        "ios-config-26=\"ip ssh server algorithm authentication publickey\"\n")
    userdata.append("ios-config-27=\"ip ssh maxstartups 1\"\n")

    userdata.append("ios-config-170=\"hostname %s\"\n" % hostname)
    userdata.append("ios-config-171=\"line vty 0 20\"\n")
    userdata.append("ios-config-172=\"login local\"\n")
    userdata.append("ios-config-173=\"transport input ssh\"\n")
    userdata.append("autoscaler-tag=\"%s\"\n" % autoscaler_tag)


    # userdata.append("ios-config-180=\"call-home\"\n")
    # userdata.append("ios-config-181=\"profile CiscoTAC-1\"\n")
    # userdata.append("ios-config-182=\"active\"\n")
    # userdata.append("ios-config-183=\"destination transport-method http\"\n")
    # userdata.append("ios-config-184=\"no destination transport-method email\"\n")

    s = ''.join(userdata)

    return s


class as_cloud():
    def __init__(self):
        self.logger = logging.getLogger('autoscaler')

        self.cloudwatch = boto3.client('cloudwatch')
        self.region = os.getenv('AWS_DEFAULT_REGION', "us-east-1")

        # todo: check to see that region is probably setup for lambda
        self.endpoint_url = {
            "us-east-1": "https://s3.amazonaws.com",
            "us-east-2": "https://s3-us-east-2.amazonaws.com",
            "us-west-1": "https://s3-us-west-1.amazonaws.com",
            "us-west-2": "https://s3-us-west-2.amazonaws.com",
            "eu-west-1": "https://s3-eu-west-1.amazonaws.com",
            "eu-central-1": "https://s3-eu-central-1.amazonaws.com",
            "ap-northeast-1": "https://s3-ap-northeast-1.amazonaws.com",
            "ap-northeast-2": "https://s3-ap-northeast-2.amazonaws.com",
            "ap-south-1": "https://s3-ap-south-1.amazonaws.com",
            "ap-southeast-1": "https://s3-ap-southeast-1.amazonaws.com",
            "ap-southeast-2": "https://s3-ap-southeast-2.amazonaws.com",
            "sa-east-1": "https://s3-sa-east-1.amazonaws.com"
        }

        self.s3_resource = boto3.resource('s3', endpoint_url=self.endpoint_url[self.region], config=Config(
            s3={'addressing_style': 'virtual'}, signature_version='s3v4'))
        self.s3_client = boto3.client('s3', endpoint_url=self.endpoint_url[self.region], config=Config(
            s3={'addressing_style': 'virtual'}, signature_version='s3v4'))
        self.sns = boto3.client('sns')
        self.ec2 = boto3.resource('ec2')
        self.ec2_client = boto3.client('ec2')
        self.events_client = boto3.client('events')

        self.Results = namedtuple('Results', 'min, max, avg, cnt, inst')

        self.privatekey_prefix = "AutoScaler/privatekeys/"


    def get_storage_prefix(self):
        if 'bucket_prefix' in os.environ:
            vpnconfig_prefix = os.environ['bucket_prefix']
        else:
            vpnconfig_prefix = "vpnconfigs/"

        return vpnconfig_prefix

    def get_as_private_key_files_info(self, instance_id):
        '''
        This method returns transit network solutions' private key files location information
        :param instance_id (str):
        :return: key_tuple (tuple object) - ( private key directory path, file name)
        '''
        return (self.privatekey_prefix, str(instance_id) + '.pem')

    def get_short_instance_id(self, instance_id):
        '''
        :param instance_id:
        :return: instance_id
        '''
        return instance_id

    def get_tnet_private_key_files_info(self, instance_id):
        '''
        This method returns Autoscaler solutions' private key files location information
        :param instance_id (str):
        :return: key_tuple (tuple object) - ( private key directory path, file name)
        '''
        return (self.get_storage_prefix(), 'prikey.pem')

    def get_transit_network_filename(self):
        return "transit_vpc_config.txt"

    def get_transit_network_config(self, storage_name, config_filename):
        vpnconfig_prefix = self.get_storage_prefix()
        self.logger.info("storage_name: %s" % storage_name)
        self.logger.info("vpnconfig_prefix: %s" % vpnconfig_prefix)
        self.logger.info("config_filename: %s" % config_filename)
        for i in range(5):
            try:
                config = ast.literal_eval(
                    self.s3_client.get_object(
                        Bucket=storage_name,
                        Key=vpnconfig_prefix +
                        config_filename)['Body'].read())
            except Exception as e:
                self.logger.warning("Exception while getting vpc config: %s" % e)
                config = None
                continue
        return config


    def put_transit_network_Config(self, status, storage_name, config_file, config):
        vpnconfig_prefix = self.get_storage_prefix()

        self.logger.info(
            "Uploading new config file: %s/%s/%s%s",
            self.endpoint_url[self.region],
            storage_name,
            vpnconfig_prefix,
            config_file)
        try:
            self.s3_client.put_object(
                Bucket=storage_name,
                Key=vpnconfig_prefix +
                config_file,
                Body=str(config),
                ACL='bucket-owner-full-control',
                ServerSideEncryption='aws:kms',
                SSEKMSKeyId=status.get_kms_key())

        except Exception as e:
            self.logger.warning("Failed to put VPC config file: %s" % e)
            return False

        return True

    def get_instanceId_from_ip(self, public_ip_address):
        try:
            addresses_dict = self.ec2_client.describe_addresses(
                PublicIps=[public_ip_address])
            return addresses_dict["Addresses"][0]['InstanceId']
        except Exception as e:
            self.logger.warning("Exception while looking up ip address: %s" % e)
            return None

    def get_instance_config_filename(self, instance_id):
        return "%s.cfg" % instance_id

    def get_private_key(self, storage_name, prikey):
        if os.path.exists('/tmp/' + prikey):
            os.remove('/tmp/' + prikey)

            self.logger.debug(
            "Downloading private key: %s/%s/%s%s",
            self.endpoint_url[self.region],
            storage_name,
            self.privatekey_prefix,
            prikey)

        try:
            self.s3_client.download_file(
                storage_name, self.privatekey_prefix + prikey, '/tmp/' + prikey)
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        return True


    def put_private_key(self, status, storage_name, instance_id, prikey):

        instance_private_key_filename = instance_id + '.pem'
        self.logger.debug(
            "Downloading private key: %s/%s/%s%s",
            self.endpoint_url[self.region],
            storage_name,
            self.privatekey_prefix,
            prikey)
        try:
            self.s3_client.put_object(
                Bucket=storage_name,
                Key=self.privatekey_prefix +
                instance_private_key_filename,
                Body=str(prikey),
                ACL='bucket-owner-full-control',
                ServerSideEncryption='aws:kms',
                SSEKMSKeyId=status.get_kms_key())
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False
        return True


    def copy_private_key(self, status, storage_name, from_file, to_file):

        try:
            self.s3_resource.Object(
                storage_name,
                self.privatekey_prefix +
                to_file).copy_from(
                CopySource=storage_name +
                '/' +
                self.privatekey_prefix +
                from_file,
                ACL='bucket-owner-full-control',
                ServerSideEncryption='aws:kms',
                SSEKMSKeyId=status.get_kms_key())
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        return True

    def copy_original_privateKey(self, status, storage_name, from_file, to_file):
        vpnconfig_prefix = self.get_storage_prefix()

        try:
            self.s3_resource.Object(
                storage_name,
                self.privatekey_prefix +
                to_file).copy_from(
                CopySource=storage_name +
                '/' +
                vpnconfig_prefix +
                'prikey.pem',
                ACL='bucket-owner-full-control',
                ServerSideEncryption='aws:kms',
                SSEKMSKeyId=status.get_kms_key())
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        return True


    def save_original_privateKey(self, status, storage_name, from_file, to_file):
        vpnconfig_prefix = self.get_storage_prefix()

        try:
            self.s3_resource.Object(
                storage_name,
                vpnconfig_prefix +
                'prikey.pem').copy_from(
                CopySource=storage_name +
                '/' +
                self.privatekey_prefix +
                from_file,
                ACL='bucket-owner-full-control',
                ServerSideEncryption='aws:kms',
                SSEKMSKeyId=status.get_kms_key())
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        return True


    def associate_role_to_instance(self, instance_id, cloud_config):
        role = cloud_config["iam_instance_profile"]
        try:
            self.ec2_client.associate_iam_instance_profile(
                IamInstanceProfile={
                    'Arn': role,
                },
                InstanceId=instance_id
            )
        except Exception as e:
            self.logger.error(
                "Not able to associate %s to %s -> %s" %
                (role, instance_id, e))
            return False

        return True

    def set_instance_tags(self, cfg, instance_id, name):
        try:
            i = self.ec2.Instance(instance_id)

            self.ec2.create_tags(Resources=[i.id], Tags=[
                {'Key': 'Name', 'Value': name}])

            self.ec2.create_tags(Resources=[i.id], Tags=[
                {'Key': 'AutoScaleGroup', 'Value': cfg.get_as_group_name()}])

            self.ec2.create_tags(Resources=[i.id], Tags=[
                {'Key': 'storage_name', 'Value': cfg.get_storage_name()}])

        except Exception as e:
            self.logger.warning(
                "Failed to set label on instance %s to %s (%s)" %
                (instance_id, name, e))
            return False

        return True

    def is_instance_ready(self, instance_id):
        try:
            response = self.ec2_client.describe_instance_status(
                Filters=[
                    {
                        'Name': 'instance-status.reachability',
                        'Values': [
                            'passed',
                        ]
                    },
                ],
                InstanceIds=[
                    instance_id,
                ],
            )
            if len(response['InstanceStatuses']):
                instance_status = response['InstanceStatuses'][0]['InstanceStatus']['Status']
            else:
                instance_status = "Not ready."
        except Exception as e:
            instance_status = "Not Ready : %s" % e

        self.logger.info("Instance %s is %s" % (instance_id, instance_status))

        if instance_status == "ok":
            return True
        else:
            return False


    def is_instance_running(self, instance_id):
        try:
            response = self.ec2_client.describe_instances(
                InstanceIds=[
                    instance_id,
                ],
            )
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        if len(response['Reservations']) == 0:
            return False

        for r in response['Reservations']:
            for i in r['Instances']:
                if i['State']['Name'] == 'running':
                    return True
        return False


    def get_running_state(self, instance_id):
        try:
            response = self.ec2_client.describe_instances(
                InstanceIds=[
                    instance_id,
                ],
            )
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return "terminated"

        if len(response['Reservations']) == 0:
            return "terminated"

        # 'Name': 'pending' | 'running' | 'shutting-down' | 'terminated' | 'stopping' | 'stopped'
        for r in response['Reservations']:
            for i in r['Instances']:
                return i['State']['Name']
        return "terminated"


    def get_reachability_status(self, instance_id):
        try:
            response = self.ec2_client.describe_instance_status(
                InstanceIds=[
                    instance_id,
                ],
            )
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return "Failed"

        if "InstanceStatuses" in response:
            for instance_response in response["InstanceStatuses"]:
                system_status = instance_response['SystemStatus']['Details'][0]['Status']
                instance_status = instance_response['InstanceStatus']['Details'][0]['Status']
                if system_status == "passed" and instance_status == "passed":
                    return "Passed"

        return "Failed"


    def put_file(self, status, storage_name, directory, filename):
        try:
            self.s3_client.upload_file(
                '/tmp/' + filename,
                storage_name,
                directory + filename,
                ExtraArgs={
                    "ServerSideEncryption": "aws:kms",
                    "SSEKMSKeyId": status.get_kms_key()})

        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        return True

    def get_file(self, storage_name, directory, filename):
        try:
            self.s3_client.download_file(
                storage_name,
                directory + filename,
                '/tmp/' + filename)
        except Exception as e:
            self.logger.warning(
                "Did not find %s:%s%s (%s)" %
                (storage_name, directory, filename, e))
            return False

        return True


    def does_file_exist(self, storage_name, filename):
        if filename is None:
            return False
        try:
            if self.s3_client.list_objects(
                    Bucket=storage_name,
                    Prefix='AutoScaler' + filename):
                return True

            return False

        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False


    def copy_file(self, status, storage_name, directory, from_file, to_file):

        try:
            self.s3_resource.Object(
                storage_name,
                directory +
                to_file).copy_from(
                CopySource=storage_name +
                '/' +
                directory +
                from_file,
                ACL='bucket-owner-full-control',
                ServerSideEncryption='aws:kms',
                SSEKMSKeyId=status.get_kms_key())

        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        return True

    # stub function to keep the parity between azure utils and aws utils
    def copy_file_from_to_dir(self, storage_name, from_dir, from_file, to_dir, to_file):
        return True

    def get_metric(
            self,
            name,
            instance_id,
            period,
            metric_period,
            metric_type,
            namespace):

        dimensions = [
            {'Name': "InstanceId",
             'Value': instance_id}
        ]
        if metric_type == "Sum":
            stats_type = ["Sum"]
        else:
            stats_type = ["Maximum"]

        response = self.cloudwatch.get_metric_statistics(
            Namespace=namespace,
            MetricName=name,
            # Unit='Count',
            Dimensions=dimensions,
            StartTime=datetime.datetime.utcnow() -
            datetime.timedelta(
                seconds=int(period)),
            EndTime=datetime.datetime.utcnow(),
            Period=metric_period,
            Statistics=stats_type,
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            mylist = []
            for dp in response['Datapoints']:
                if metric_type == "Sum":
                    value = (dp[stats_type[0]]) / metric_period
                else:
                    value = dp[stats_type[0]]
                mylist.append((name, dp['Timestamp'], value))

            if len(mylist):
                results = sorted(mylist, key=lambda x: x[0])
                name, min_time, min_value = min(
                    results, key=lambda item: item[2])
                name, max_time, max_value = max(
                    results, key=lambda item: item[2])
                avg_value = (sum(x[2] for x in results) / len(mylist))
                self.logger.debug("%s (%s) => %s/%s/%s" %
                             (instance_id, name, min_value, max_value, avg_value))

                result = self.Results(
                    min=min_value,
                    max=max_value,
                    avg=avg_value,
                    cnt=len(mylist),
                    inst=instance_id)

                return result
            else:
                self.logger.debug("No Datapoints for %s (%s)" % (instance_id, name))
        else:
            self.logger.warning("Bad response: %s" % response)
        return None


    def put_metric(self, name, description, group_name):
        try:
            response = self.cloudwatch.put_metric_data(
                Namespace="csr1000v",
                MetricData=[{'MetricName': name,
                             'Value': 1,
                             'Unit': 'Count',
                             'Dimensions': [
                                 {
                                     'Name': "AutoScaleGroup",
                                     'Value': group_name
                                 },
                                 {
                                     'Name': "Action",
                                     'Value': description
                                 }
                             ]
                             }
                            ],
            )
            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                self.logger.warning("Bad response for %s: %s" % (name, response))
                return False
            return True

        except Exception as e:
            self.logger.warning("Exception %s" % e)
            return False

        return True

    def send_notification(
            self,
            topicarn,
            msg="",
            subject="",
            msgtype='string',
            message_attributes={}):

        self.logger.info("topicarn: %s" % topicarn)
        self.logger.info("msg: %s" % msg)
        self.logger.info("subject: %s" % subject)
        self.logger.info("message_attributes: %s" % message_attributes)
        try:
            response = self.sns.publish(
                TopicArn=topicarn,
                Subject=subject,
                Message=msg,
                MessageStructure=msgtype,
                MessageAttributes=message_attributes

            )
            self.logger.info("response from sending notification: %s" % response)
        except Exception as e:
            self.logger.warning("Failed to send notification: %s" % e)
            response = e

        self.logger.info("Done sending response")
        return response

    def send_user_notification(self, cloud_config,
                                        msg="",
                                        subject="",
                                        msgtype='string',
                                        message_attributes={}):
        if 'TopicArn' in cloud_config:
            topicarn = cloud_config['TopicArn']
        else:
            self.logger.info("No Notification ARN found in cloud config")
            return "Not Sent"

        self.send_notification(topicarn, msg=msg,
                                        subject=subject,
                                        msgtype='string',
                                        message_attributes=message_attributes)

    def put_rule(self, arn, minutes):

        try:
            response = self.events_client.list_rule_names_by_target(
                TargetArn=arn,
            )
            for rule_name in response['RuleNames']:
                name = rule_name
                break
            else:
                return False
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        if minutes > 1:
            frequency = "rate(%d minutes)" % int(minutes)
        else:
            frequency = "rate(%d minute)" % int(minutes)

            self.logger.info("frequency: %s" % frequency)
        try:
            rule_response = self.events_client.put_rule(
                Name=name,
                ScheduleExpression=frequency,
                State='ENABLED',
            )
            self.logger.info("%s" % rule_response)
        except Exception as e:
            self.logger.warning("Exception putting rule: %s" % e)


    def get_rule_minutes(self, arn):
        try:
            response = self.events_client.list_rule_names_by_target(
                TargetArn=arn,
            )
            for rule_name in response['RuleNames']:
                name = rule_name
                break
            else:
                return None
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False

        try:
            rule_response = self.events_client.describe_rule(
                Name=name
            )
            self.logger.info("%s" % rule_response)
        except Exception as e:
            self.logger.warning("Exception getting rule: %s" % e)
            return 999

        expression = rule_response['ScheduleExpression']
        numbers = re.findall(r'\d+', expression)
        return int(numbers[0])


    def get_cloud_cfg_subset(self, instance_id, default_cfg=None):
        cloud_config = {}
        az_list = []
        subnet_list = []
        sec_group_list = []
        try:
            ec2 = boto3.resource('ec2')

            i = ec2.Instance(instance_id)
            az_list.append(i.placement["AvailabilityZone"])

            for network_interface in i.network_interfaces_attribute:
                subnet_list.append(network_interface["SubnetId"])
                for group in network_interface['Groups']:
                    sec_group_list.append(group["GroupId"])

            cloud_config["instance_type"] = i.instance_type
            # todo: get appropriate image
            cloud_config["ami-id"] = i.image_id
            cloud_config["key_name"] = i.key_name
            cloud_config["az_list"] = az_list
            cloud_config["subnet_id"] = subnet_list
            cloud_config["security_groups"] = sec_group_list
            if i.iam_instance_profile is not None:
                cloud_config["iam_instance_profile"] = i.iam_instance_profile['Arn']
            else:
                cloud_config["iam_instance_profile"] = "Unknown"
                self.logger.warning(
                    "Currently, instance %s does not have an instance profile" %
                    instance_id)

            cloud_config["public_ip_address"] = i.public_ip_address
            cloud_config["private_ip_address"] = i.private_ip_address
            self.logger.debug(
                "Instance %s config =\n %s\n" %
                (instance_id, cloud_config))
            return cloud_config
        except Exception as e:
            self.logger.warning("Failed to get config for %s (%s)" % (instance_id, e))
            return default_cfg


    def get_cloud_config(self, instance_id):
        return self.get_cloud_cfg_subset(instance_id)

    def get_public_ip(self, instance_id, saved_config):
        if saved_config and "public_ip_address" in saved_config:
            return saved_config["public_ip_address"]
        else:
            config = self.get_cloud_config(instance_id)
            return config["public_ip_address"]

    def get_image_id(self, instance_id, saved_config):
        if saved_config and "ami-id" in saved_config:
            return saved_config["ami-id"]
        else:
            config = self.get_cloud_config(instance_id)
            return config["ami-id"]

    def get_ip_allocation_id(self, instance_id):
        config = self.get_cloud_config(instance_id)
        ip_address = config["public_ip_address"]
        try:
            response = self.ec2_client.describe_addresses(
                PublicIps=[
                    ip_address
                ],
            )
            return response["Addresses"][0]['AllocationId']
        except:
            return None


    def reserve_ip(self, name=None):
        try:
            eip = self.ec2_client.allocate_address(Domain='vpc')
            elastic_ip = eip['PublicIp']
            allocationId = eip["AllocationId"]
        except Exception as e:
            self.logger.info("Elastic IP was not created, Error: %s ", e)
            elastic_ip = None
            allocationId = None

        return elastic_ip, allocationId


    def associate_ip(self, instance_id, allocationId):
        try:
            self.ec2_client.associate_address(
                InstanceId=instance_id,
                AllocationId=allocationId)
        except Exception as e:
            self.logger.info("Could not associate ip for %s (%s)" % (instance_id, e))
            return False

        return True

    def disassociate_ip(self, instance_id, allocation_id):
        try:
            self.ec2_client.disassociate_address(
                AssociationId=allocation_id
            )

        except Exception as e:
            self.logger.info("Could not disassociate ip for %s (%s)" % (instance_id, e))
            return False

        return True

    def release_ip(self, instance_id):
        allocationid = self.get_ip_allocation_id(instance_id)
        if allocationid is None:
            self.logger.info("Can not release ip for instance %s" % instance_id)
            return False

        self.disassociate_ip(instance_id, allocationid)
        try:
            eip = self.ec2_client.release_address(
                AllocationId=allocationid)
        except Exception as e:
            self.logger.exception("Exception: %s" % e)
            return False
        self.logger.info("Eip:%s" % eip)
        return True


    def spin_up_csr(self, cfg, status, image_id, name, allocationId, fingerprint, tag):
        inst_num = int(name.rsplit('-', 1)[1])
        self.logger.info("Instance Number: %d" % inst_num)

        ud = create_userdata(cfg, status, inst_num, fingerprint, tag)
        logger.info("Userdata: %s", ud)

        cloud_config = cfg.get_default_instance_config()
        self.logger.info("Cloud Config: %s" % cloud_config)

        num_az = len(cloud_config["az_list"])
        which_az = (inst_num-1) % num_az
        az_zone = cloud_config["az_list"][which_az]
        subnetId = cloud_config["subnet_id"][which_az]
        self.logger.info(
            "num_az %d, which_az %d, az_zone %s" %
            (num_az, which_az, az_zone))


        iam_instance_profile = {}
        iam_instance_profile['Arn'] = cloud_config["iam_instance_profile"]

        self.logger.info("Cloud Config: %s" % cloud_config)



        try:
            csr_list = self.ec2.create_instances(
                ImageId=image_id,
                InstanceType=cloud_config["instance_type"],
                KeyName=cloud_config["key_name"],
                MaxCount=1,
                MinCount=1,
                Placement={
                    'AvailabilityZone': az_zone
                },
                SecurityGroupIds=[cloud_config["security_groups"]],
                SubnetId=subnetId,
                UserData=ud,
                DisableApiTermination=False,
                IamInstanceProfile=iam_instance_profile,
                InstanceInitiatedShutdownBehavior='stop',
            )
        except Exception as e:
            self.logger.exception("EXCEPTION: %s" % e)
            return None, None

        csr = csr_list[0]

        csr.wait_until_running()

        self.set_instance_tags(cfg, csr.id, name)

        response = self.ec2_client.modify_instance_attribute(
            SourceDestCheck={
                'Value': False
            },
            InstanceId=csr.id
        )

        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            self.logger.warning("Bad response for SourceDestCheck: %s" % response)

        if cloud_config['DisableApiTermination'] == "Yes":
            response = self.ec2_client.modify_instance_attribute(
                DisableApiTermination={
                    'Value': True
                },
                InstanceId=csr.id
            )

            if response['ResponseMetadata']['HTTPStatusCode'] != 200:
                self.logger.warning(
                    "Bad response for DisableApiTermination: %s" %
                    response)

        # todo: what if the following fails
        csr.wait_until_running()

        return csr.id


    def spin_down_csr(self, instance_list, config):
        waiter = self.ec2_client.get_waiter('instance_terminated')

        for instance_id in instance_list:
            try:
                instance = self.ec2.Instance(instance_id)
                # if termination protection is enabled, disable it before
                # terminating.
                response = instance.describe_attribute(
                    Attribute='disableApiTermination')
                if response['DisableApiTermination']['Value']:
                    response = instance.modify_attribute(DisableApiTermination={
                        'Value': False
                    })
                    self.logger.info("%s" % response)

                response = instance.terminate()
                self.logger.info("%s" % response)

            except Exception as e:
                self.logger.error("Failed to Terminate: %s" % e)
                return False

        waiter.wait(InstanceIds=instance_list)

        return True


    def reboot_instance(self, instance_id):
        try:
            response = self.ec2_client.reboot_instances(
                InstanceIds=[
                    instance_id
                ],
            )

            self.logger.info("Rebooted instance %s" % instance_id)
            self.logger.debug("%s" % response)

        except Exception as e:
            self.logger.error("Failed to reboot instance %s: %s" % (instance_id, e))
            return False

        return True


    def clean_storage(self, storage_name):
        bucket = self.s3_resource.Bucket(storage_name)

        for s3_file in bucket.objects.filter(Prefix=self.privatekey_prefix):
            instance_id = (os.path.basename(s3_file.key).split('.')[0])
            if self.get_running_state(instance_id) == "terminated":
                try:
                    self.s3_client.delete_object(
                        Bucket=storage_name,
                        Key=s3_file.key,
                    )
                    self.logger.info("Deleted %s file" % (s3_file.key))
                except Exception as e:
                    self.logger.exception("Exception: %s" % e)
                    pass
            else:
                self.logger.info(
                    "Instance %s is not terminated.  No need to delete pem file" %
                    instance_id)


    def update_function(self, function_name, storage_name, key_name):
        client = boto3.client('lambda')

        try:
            response = client.update_function_code(
                FunctionName=function_name,
                S3Bucket=storage_name,
                S3Key=key_name,
                # S3ObjectVersion='string',
                Publish=True,
                # RevisionId='string'
            )
        except Exception as e:
            self.logger.error("Failed to upgrade function %s: %s" % (function_name, e))
            return False

        self.logger.info("Updated function %s" % response)
        return True

    def is_csr_image_version_16_9_1(self, image_id):
        try:
            response = self.ec2_client.describe_images(
                Filters=[
                    {
                        'Name': 'image-id',
                        'Values': [
                            image_id,
                        ]
                    },
                ]
            )
            image_name = response['Images'][0]['Name']
            self.logger.info("Image name is %s" % image_name)
            if "cisco-CSR-." in image_name:
                parts = image_name.split("cisco-CSR-.")
                version = parts[1].split('.')
                major = version[0]
                minor = version[1]
                point = version[2].split('-')[0]
                if major == '16' and minor == '09' and point == '01a':
                    self.logger.info("Version 16.09.01a image. Returning True")
                    return True
                else:
                    self.logger.info("Version is different than 16.09.01a. Returning False")
                    return False
            else:
                self.logger.info("Private image or image name does not contain 'cisco-CSR' string. Returning False")
                return False

        except Exception as e:
            self.logger.exception("Version not found in image name. Exception is %s \nReturning False" % e)
            return False

    def configure_dmvpn_hub(self, status, instance_id):
        '''
        Get dmvpn_hub_config.txt from S3 bucket and write to a jon object
        Add CSR + instance number Eg. CSR1 to the json object
        Get Lambda ARN from dmvpn_hub_config.txt
        invoke lambda to configure CSR as DMVPN hub
        '''
        try:
            lambda_client = boto3.client('lambda')
            bucket_name = status.storage_name
            s3_prefix = self.get_storage_prefix()
            dmvpnConfig = ast.literal_eval(
                self.s3_client.get_object(Bucket=bucket_name, Key=s3_prefix + 'dmvpn_hub_config.txt')[
                    'Body'].read())
            lambda_function = dmvpnConfig['dmvpn_lambda']
            csr_num = status.get_instance_number(instance_id)
            payload = {}
            payload['dmvpnParams'] = dmvpnConfig
            payload['csr'] = 'CSR%d' % csr_num
            tmp = {}
            eip = status.get_instance_ip(instance_id)
            pip = status.get_instance_private_ip(instance_id)
            tmp['EIP%d' % csr_num] = eip
            tmp['PIP%d' % csr_num] = pip
            self.s3_client.put_object(
            Bucket=bucket_name,
            Key=s3_prefix + 'scale_out_csr_config_tmp_{}.txt'.format(csr_num),
            Body=str(tmp),
            ACL='bucket-owner-full-control',
            ServerSideEncryption='aws:kms',
            SSEKMSKeyId=status.get_kms_key())
            payload['eip'] = eip
            logger.info("Payload: {}".format(payload))
            res = lambda_client.invoke(FunctionName=lambda_function,
                                       InvocationType='RequestResponse',
                                       Payload=json.dumps(payload))
            logger.info("Configure Hub Lambda response: {}".format(res))
        except Exception as e:
            logger.exception("Exception in configure_dmvpn_hub: {}".format(e))