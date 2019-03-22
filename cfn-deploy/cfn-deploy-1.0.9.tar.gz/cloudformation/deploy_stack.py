import json
import re
import sys
import time

import boto3
import botocore
from botocore.exceptions import ClientError

from .deploy_stack_dict import deploy_status


def deploy(stack_name, template, parameters=None, capabilities=None, config=None):  # nopep8
    """Update or create a cloudformation stack.

    Parameters
    ----------
    stack_name : str
        Name of the stack to be created/updated.
    template : str
        Filename of the cloudformation template to deploy.
    parameters : list
        A list of `Parameter` structures that specify the input parameters for
        the stack.
        (dict)
            ParameterKey : str
            ParameterValue : str
            UsePreviousValue : boolean
            ResolvedValue : str
    capabilities : list
        In some cases, you must explicity acknowledge that your stack template
        contains certain capabilities in order for AWS CloudFormation to
        create the stack. Options are:
            * CAPABILITY_IAM
            * CAPABILITY_NAMED_IAM
    config : dict
        aws_access_key_id : str
        aws_secret_access_key : str
        aws_session_token : str
        region : str
    """
    if config:
        cf_client = boto3.client(
            'cloudformation',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            aws_session_token=config['aws_session_token'],
            region_name=config['region'],
        )
        r53_client = boto3.client(
            'route53',
            aws_access_key_id=config['aws_access_key_id'],
            aws_secret_access_key=config['aws_secret_access_key'],
            aws_session_token=config['aws_session_token'],
            region_name=config['region'],
        )
    else:
        cf_client = boto3.client('cloudformation')
        r53_client = boto3.client('route53')

    template_data = _parse_template(cf_client, template)

    params = {
        'StackName': stack_name,
        'TemplateBody': template_data
    }

    if capabilities:
        params['Capabilities'] = capabilities
    if parameters:
        params['Parameters'] = parameters

    try:
        if _stack_exists(cf_client, stack_name):
            print("Updating {}".format(stack_name))
            cf_client.update_stack(**params)
            stack = cf_client.describe_stacks(
                StackName=stack_name)['Stacks'][0]
        else:
            print("Creating {}".format(stack_name))
            cf_client.create_stack(**params)
            stack = cf_client.describe_stacks(
                StackName=stack_name)['Stacks'][0]
        _wait(cf_client, r53_client, stack_name)
    except botocore.exceptions.ClientError as ex:
        error_message = ex.response['Error']['Message']
        if error_message == 'No updates are to be performed.':
            print("No changes")
        else:
            raise

    return cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]


def _wait(cf_client, r53_client, stack_name):
    """Wait for a cloudformation stack deploy to complete.

    Parameters
    ----------
    stack_name : str
        Name of the stack to montior.
    """
    max_attempts = 120
    delay = 30
    num_attempts = 0
    cnames = []

    print("Waiting for stack to be ready...")
    while True:
        num_attempts += 1
        # query stack status
        stack = cf_client.describe_stacks(StackName=stack_name)['Stacks'][0]
        if deploy_status[stack['StackStatus']]['success']:
            # check if there are any certificates to create
            _register_certificates(
                cf_client,
                r53_client,
                stack_name,
                cnames
            )
        else:
            # deploy failed, remove certificates
            for cname in cnames:
                _rollback_certificate_cname(
                    r53_client,
                    cname['domain'],
                    cname['name']
                )

        if deploy_status[stack['StackStatus']]['state'] == 'complete':
            if deploy_status[stack['StackStatus']]['success']:
                print("Deploy complete")
                return
            else:
                raise Exception("Deployment failed: {} ({})".format(
                    stack['StackStatus'], stack['StackStatusReason']))

        if num_attempts >= max_attempts:
            raise Exception('Max attempts exceeded')

        time.sleep(delay)


def _register_certificates(cf_client, r53_client, stack_name, cnames):  # nopep8
    """Register ACM certificates created in the .

    Scans the events of the deployment for ACM certificates that can be
    registered in a Route53 hosted zone.  Certificates that belong to domains
    not registered to Route53 or require email validation must be validated
    manually.

    Parameters
    ----------
    stack_name : str
        Name of the stack to monitor.
    """
    # look through all resources in the related stacks
    stacks = [stack_name]
    _get_child_stacks(cf_client, stack_name, stacks)
    for stack in stacks:
        stack_event_paginator = cf_client.get_paginator(
            'describe_stack_events')
        event_pages = stack_event_paginator.paginate(StackName=stack)

        event_filter = 'StackEvents[?ResourceType == `AWS::CertificateManager::Certificate`]'  # nopep8
        events = event_pages.search(event_filter)
        for event in events:
            # don't create duplicates
            if not list(filter(lambda c: c['id'] == event['LogicalResourceId'], cnames)):  # nopep8
                _parse_reason(r53_client, event, cnames)


def _get_child_stacks(cf_client, stack_name, stacks):
    stack_resource_paginator = cf_client.get_paginator('list_stack_resources')
    resource_pages = stack_resource_paginator.paginate(StackName=stack_name)
    resource_filter = 'StackResourceSummaries[?ResourceType == `AWS::CloudFormation::Stack`].LogicalResourceId'  # nopep8
    stack_names = resource_pages.search(resource_filter)
    for child_stack in stack_names:
        stacks.append(child_stack)
        _get_child_stacks(cf_client, child_stack, stacks)


def _parse_reason(r53_client, event, cnames):
    if 'ResourceStatusReason' not in event:
        return

    # extract the values from the status
    status_text = re.search(
        r'{Name: (.*),Type: (.*),Value: (.*)}',
        event['ResourceStatusReason'],
        re.M
    )

    if status_text:
        print('Attempting to register certificate...')
        name = status_text.group(1)
        domain = name.split('.', 2)[2]
        value = status_text.group(3)
        cname = {
            'id': event['LogicalResourceId'],
            'domain': domain,
            'name': name,
            'value': value
        }

        _create_certificate_cname(
            r53_client,
            domain,
            cname['name'],
            cname['value']
        )
        cnames.append(cname)


def _get_hostedzone_id(r53_client, domain):
    """Get the hosted zone id for a Route53 domain.

    Parameters
    ----------
    domain : str
        Name of the domain to locate.

    Returns
    -------
    str or None
        HostedZoneId of the Route53 hosted zone or None if it doesn't exist.
    """
    hosted_zones = r53_client.list_hosted_zones()['HostedZones']
    print("Searching for hosted zone {}".format(domain))
    for hosted_zone in hosted_zones:
        if hosted_zone['Name'] == domain:
            return hosted_zone['Id']

    return None


def _create_certificate_cname(r53_client, domain, name, value):
    """Create the CNAME record in Route53 to validate the certificate.

    Parameters
    ----------
    domain : str
        Name of the domain to create the CNAME record.
    name : str
        Name of the record to create.
    value : str
        Value to assign to the record.
    """
    # get the hosted zone ID
    hostedZoneId = _get_hostedzone_id(r53_client, domain)

    if hostedZoneId is None:
        print((
            "Stack will not complete successfully until the DNS record Name='{"
            "}',Type='CNAME',Value='{}' has been added to your DNS database. S"
            "ee https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-valida"
            "te-dns.html for more information."
        ).format(name, value))
    else:
        print("Creating certificate: {}".format(name))

        r53_client.change_resource_record_sets(
            HostedZoneId=hostedZoneId,
            ChangeBatch={
                'Comment': 'ACM Certificate key',
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': name,
                            'Type': 'CNAME',
                            'TTL': 300,
                            'ResourceRecords': [
                                {
                                    'Value': value
                                },
                            ],
                        }
                    },
                ]
            }
        )


def _rollback_certificate_cname(r53_client, domain, name):
    """Removes CNAME created during deployment.

    Parameters
    ----------
    domain : str
        Name of domain where the CNAME was created.
    name : str
        Name of the record to remove.
    """
    hostedZoneId = _get_hostedzone_id(r53_client, domain)

    r53_client.change_resource_record_sets(
        HostedZoneId=hostedZoneId,
        ChangeBatch={
            'Changes': [
                {
                    'Action': 'DELETE',
                    'ResourceRecordSet': {
                        'Name': name,
                        'Type': 'CNAME'
                    }
                },
            ]
        }
    )


def _parse_template(cf_client, template):
    """Parse and validate the cloudformation template file.

    Parameters
    ----------
    cf_client : object
        Cloudformation client for performing stack operations.
    template : str
        Filename of the cloudformation template.

    Returns
    -------
    str
        Cloudformation template data.
    """
    with open(template) as template_fileobj:
        template_data = template_fileobj.read()
    cf_client.validate_template(TemplateBody=template_data)
    return template_data


def _parse_parameters(parameters):
    """Parse the cloudformation parameters file.

    Parameters
    ----------
    parameters : str
        Filename of the parameters file.
    Returns
    -------
    str
        Cloudformation parameter data.
    """
    with open(parameters) as parameter_fileobj:
        parameter_data = json.load(parameter_fileobj)
    return parameter_data


def _stack_exists(cf_client, stack_name):
    """Determine if the stack already exists.

    Parameters
    ----------
    stack_name : str
        Name of the stack to find.

    Returns
    -------
    bool
        True if the stack already exists.
    """
    stacks = cf_client.list_stacks()['StackSummaries']
    for stack in stacks:
        if stack['StackStatus'] == 'DELETE_COMPLETE':
            continue
        if stack_name == stack['StackName']:
            return True
    return False


def undeploy(stack_name):
    """Remove a cloudformation stack.

    Parameters
    ----------
    stack_name : str
        Name of the stack to remove.
    """
    max_attempts = 120
    delay = 30
    num_attempts = 0

    print("Waiting for stack to be deleted...")
    cf = boto3.client('cloudformation')
    cf.delete_stack(StackName=stack_name)
    while True:
        num_attempts += 1
        # query stack status
        try:
            stacks = cf.describe_stacks(StackName=stack_name)['Stacks']
            if len(stacks) == 0:
                print("Delete complete")
                return

            if stacks[0]['StackStatus'] == 'DELETE_FAILED':
                print("Failed to delete stack: {}".format(
                    stacks[0]['StackStatusReason']))
                raise Exception('Stack deletion failed')

            elif stacks[0]['StackStatus'] == 'DELETE_COMPLETE':
                print("Delete complete")
                return

        except ClientError as e:
            if e.response['Error']['Message'] == "Stack with id {} does not exist".format(stack_name):  # nopep8
                # stack doesn't exist
                print("Delete complete")
                return
            else:
                raise e

        sys.stdout.write('.')
        time.sleep(delay)

        if num_attempts >= max_attempts:
            raise Exception('Max attempts exceeded')
