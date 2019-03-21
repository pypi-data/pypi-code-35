# coding=utf-8
from __future__ import print_function
import argparse
import logging
import urllib3
from ibm_ai_openscale_cli.enums import ResetType, MLEngineType
from ibm_ai_openscale_cli import logging_temp_file, name
from ibm_ai_openscale_cli.environments import Environments
from ibm_ai_openscale_cli.openscale.openscale_reset import ResetType
from ibm_ai_openscale_cli.openscale_ops import OpenScaleOps
from ibm_ai_openscale_cli.reset_ops import ResetOps
from ibm_ai_openscale_cli.version import __version__
from outdated import warn_if_outdated

logger = logging.getLogger(__name__)

SERVICE_NAME = 'Watson OpenScale'

def get_argument_parser():
    """
    generate a CLI arguments parser
    Returns:
       argument parser
    """
    description ='IBM Watson Openscale "fastpath" configuration tool. This tool allows the user to get started quickly with Watson OpenScale: 1) If needed, provision a Lite plan instance for IBM Watson OpenScale\n2) If needed, provision a Lite plan instance for IBM Watson Machine Learning\n3) Drop and re-create the IBM Watson OpenScale datamart instance and datamart database schema\n4) Optionally, deploy a sample machine learning model to the WML instance\n5) Configure the sample model instance to OpenScale, including payload logging, fairness checking, feedback, quality checking, and explainability\n6) Optionally, store up to 7 days of historical payload, fairness, and quality data for the sample model'
    parser = argparse.ArgumentParser(description=description)
    # required parameters
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('-a', '--apikey', help='IBM Cloud platform user APIKey. If "--env icp" is also specified, APIKey value is not used. ', required=True)
    # Optional parameters
    optional_args = parser._action_groups.pop()
    parser.add_argument('--env', default='ypprod', help='Environment. Default "ypprod"', choices=['ypprod', 'ypqa', 'ys1dev', 'icp'])
    parser.add_argument('--resource-group', default='default', help='Resource Group to use. If not specified, then "default" group is used')
    parser.add_argument('--postgres', help='Path to postgres credentials file for the datamart database. If --postgres, --icd, and --db2 all are not specified, then the internal {} database is used'.format(SERVICE_NAME))
    parser.add_argument('--postgres-json', help='Postgres credentials in JSON format')
    parser.add_argument('--icd', help='Path to IBM Cloud Database credentials file for the datamart database')
    parser.add_argument('--icd-json', help='IBM Cloud Database credentials for the datamart database in JSON format')
    parser.add_argument('--db2', help='Path to IBM DB2 credentials file for the datamart database')
    parser.add_argument('--db2-json', help='IBM DB2 credentials for the datamart database in JSON format:  \'{ "username": "<USERNAME>", "password": "<PASSWORD>", "hostname": "<hostname>", "port": "<port>", "db": "<db>" }\'')
    parser.add_argument('--wml', help='Path to IBM WML credentials file')
    parser.add_argument('--wml-json', help='IBM WML credentials in JSON format')
    parser.add_argument('--azure', help='Path to Microsoft Azure credentials file')
    parser.add_argument('--azure-json', help='Microsoft Azure credentials in JSON format: \'{ "client_id": "<CLIENT_ID", "client_secret": "<CLIENT_SECRET", "tenant": "<TENANT>", "subscription_id": "<SUBSCRIPTION_ID" }\'')
    parser.add_argument('--spss', help='Path to SPSS credentials file')
    parser.add_argument('--spss-json', help='SPSS credentials in JSON format: \'{ "username": "<USERNAME>", "password": "<PASSWORD", "url": "<URL>" }\'')
    parser.add_argument('--custom', help='Path to Custom Engine credentials file')
    parser.add_argument('--custom-json', help='Custom Engine credentials in JSON format: \'{ "url": "<URL>" }\'')
    parser.add_argument('--aws', help='Path to Amazon Web Services credentials file')
    parser.add_argument('--aws-json', help='Amazon Web Services credentials in JSON format: \'{ "access_key_id": "<ACCESS_KEY_ID", "secret_access_key": "<SECRET_ACCESS_KEY", "region": "<REGION>" }\'')
    parser.add_argument('--deployment-name', help='Name of the existing deployment to use. Required for Azure ML Studio, SPSS Engine and Custom ML Engine. Optional for Watson Machine Learning')
    parser.add_argument('--username', help='ICP username. Required if "icp" environment is chosen')
    parser.add_argument('--password', help='ICP password. Required if "icp" environment is chosen')
    parser.add_argument('--url', help='ICP url. Required if "icp" environment is chosen')
    parser.add_argument('--datamart-name', default='aiosfastpath', help='Specify data mart name and database schema, default is "aiosfastpath"')
    parser.add_argument('--keep-schema', action='store_true', help='Use pre-existing datamart schema, only dropping all tables. If not specified, datamart schema is dropped and re-created')
    parser.add_argument('--history', default=7, help='Days of history to preload. Default is 7', type=int)
    parser.add_argument('--verbose', action='store_true', help='verbose flag')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))
    parser.add_argument('--model', default='GermanCreditRiskModel', help='Model to set up with Watson OpenScale (default "GermanCreditRiskModel")', choices=['all', 'GermanCreditRiskModel', 'DrugSelectionModel', 'GolfModel'])
    parser.add_argument('--custom-model', help=argparse.SUPPRESS) # help='Name of custom model to set up with Watson OpenScale. If specified, overrides the value set by --model. Also requires that --custom-model-directory be specified')
    parser.add_argument('--custom-model-directory', help=argparse.SUPPRESS) #help='Directory with model configuration and metadata files. Also requires that --custom-model be specified')
    parser.add_argument('--training-data-json', help=argparse.SUPPRESS)
    parser.add_argument('--bx', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--extend', action='store_true', help=argparse.SUPPRESS) # Extend existing datamart. If not specified and the datamart already exists, it will be deleted and recreated. Currently only supported for WML.
    parser.add_argument('--reset', choices=['metrics', 'monitors', 'datamart', 'model'], help='Reset existing datamart then exit')
    parser.add_argument('--model-first-instance', default=1, help=argparse.SUPPRESS, type=int) # First "instance" (copy) of each model. Default 1 means to start with the base model instance
    parser.add_argument('--model-instances', default=1, help=argparse.SUPPRESS, type=int) # Number of additional instances beyond the first.
    parser.add_argument('--sync-checks', action='store_true', help=argparse.SUPPRESS) # If true, make fairness and quality checks synchronous (default is asynchronous)
    parser.add_argument('--organization', help=argparse.SUPPRESS, required=False)
    parser.add_argument('--space', help=argparse.SUPPRESS, required=False)
    parser._action_groups.append(optional_args)
    return parser

def initialize(args):
    """
    Initialize and validate necessary entities
    """
    def _validate_deployment_name_specified(deployment_name, model_name=None, env_name='ypprod'):
        if args.ml_engine_type is MLEngineType.WML:
            if deployment_name and model_name == 'all':
                logger.error('ERROR: A model name is required when a deployment is specified for {}'.format(args.ml_engine_type.value))
                exit(1)
        else:
            if not deployment_name:
                logger.error('ERROR: A deployment name is required when {} is used with {}'.format(SERVICE_NAME, args.ml_engine_type.value))
                exit(1)

    def _validate_is_icp(env_name):
        if not env_name == 'icp':
            logger.error('ERROR: {} is only supported on {} on IBM Cloud Private (ICP)'.format(SERVICE_NAME, args.ml_engine_type.value))
            exit(1)

    # validate environment
    if 'throw' in args:
        logger.error(args.throw)
        exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.getLogger('handle_response').setLevel(logging.DEBUG)
        logging.getLogger('ibm_ai_openscale.utils.client_errors').setLevel(logging.DEBUG)

    # setup the loger
    logger.info('ibm-ai-openscale-cli-{}'.format(__version__))
    logger.info('Log file: {0}'.format(logging_temp_file.name))

    # outdated packages
    warn_if_outdated(name, __version__)

    # initialize args
    args.is_icp = False
    args.service_name = SERVICE_NAME
    if args.azure or args.azure_json:
        args.ml_engine_type = MLEngineType.AZUREML
        _validate_deployment_name_specified(args.deployment_name)
    elif args.spss or args.spss_json:
        args.ml_engine_type = MLEngineType.SPSS
        _validate_is_icp(args.env)
        _validate_deployment_name_specified(args.deployment_name)
    elif args.custom or args.custom_json:
        args.ml_engine_type = MLEngineType.CUSTOM
        _validate_deployment_name_specified(args.deployment_name)
    elif args.aws or args.aws_json:
        args.ml_engine_type = MLEngineType.SAGEMAKER
        _validate_deployment_name_specified(args.deployment_name)
    else:
        args.ml_engine_type = MLEngineType.WML
        _validate_deployment_name_specified(args.deployment_name, args.model, args.env)
    env_dict = Environments(args).get_attributes()
    args.env_dict = env_dict
    if args.reset:
        args.reset_type = ResetType(args.reset)
    if args.env == 'icp':
        args.is_icp = True
        logger.info('SSL verification is not used for requests against ICP Environment, disabling "InsecureRequestWarning"')
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def show_finish_prompt(dashboard_url):
    logger.info('Process complete')
    if dashboard_url.startswith('https://api.'):
        dashboard_url = dashboard_url.replace('https://api.', 'https://')
    logger.info('The {} dashboard can be accessed at: {}/aiopenscale'.format(SERVICE_NAME, dashboard_url))

def main(arguments=None):

    args = arguments if arguments else get_argument_parser().parse_args()
    initialize(args)

    # operations
    if args.reset:
        ResetOps(args).execute()
    else:
        OpenScaleOps(args).execute()

    # finish
    show_finish_prompt(args.env_dict['aios_url'])
