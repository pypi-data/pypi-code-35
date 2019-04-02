# coding=utf-8
from __future__ import print_function
import os
import argparse
import json
import logging
import requests
import urllib3
import yaml
import subprocess
from collections import OrderedDict
from ibm_apidocs_cli.version import __version__
from lxml import html
from outdated import warn_if_outdated

logger = logging.getLogger(__name__)

def get_argument_parser():
    """
    generate a CLI arguments parser
    Returns:
       argument parser
    """
    parser = argparse.ArgumentParser(description='Generate the apidocs files.')
    # required parameters
    requiredArgs = parser.add_argument_group('Required arguments')
    requiredArgs.add_argument('-i', '--openapi', help='Input OpenAPI specification file path or url', required=True)
    requiredArgs.add_argument('-a', '--apidocs', help='Path to apidocs repository containing config files')
    requiredArgs.add_argument('-c', '--config', help='Name of front matter config file', required=True)
    # Optional parameters
    optionalArgs = parser._action_groups.pop()
    parser.add_argument('--frontmatter', default='https://github.ibm.com/cloud-doc-build/frontmatter-generator', help='Frontmatter repository or local CLI')
    parser.add_argument('--sdk_generator', metavar='sdk-generator', default='https://github.ibm.com/CloudEngineering/openapi-sdkgen', help='Path to SDK generator JAR. If not specified the public release will be use')
    parser.add_argument('--output_folder', metavar='output-folder', default='build', help='Generated apidocs output folder')
    parser.add_argument('--verbose', action='store_true', help='verbose flag')
    parser.add_argument('--version', action='version', version='%(prog)s {version}'.format(version=__version__))

    parser._action_groups.append(optionalArgs)
    return parser

def process_args(parser):
    """
    Parses the parser
    Returns:
        dict -- dictionary with the arguments and values
    """
    args = parser.parse_args()

    # validate environment
    if 'throw' in args:
        logger.error(args.throw)
        exit(1)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    return args

def main():
    parser = get_argument_parser()
    args = process_args(parser)

    # Get the open api filename assistant-v2 from (./public/assistant-v2.json)
    openapi_file = get_basename(args.openapi)
    config_file = args.config
    frontmatter_cli = get_frontmatter_cli(args.frontmatter)
    sdk_generator_cli = get_sdk_generator_cli(args.sdk_generator)
    supported_languages = get_supported_languages(args.openapi)

    if (os.path.dirname(args.config) == ''):
      input_frontmatter_config = os.path.join(args.apidocs, args.config)
    else:
      input_frontmatter_config = args.config
    output_frontmatter_config = os.path.join(args.output_folder, os.path.basename(args.config))

    frontmatter_md_file = '%s/%s.md' % (args.output_folder, openapi_file)

    logger.info('openapi_file: %s' % openapi_file)
    logger.info('config_file: %s' % config_file)
    logger.info('frontmatter_cli: %s' % frontmatter_cli)
    logger.info('sdk_generator_cli: %s' % sdk_generator_cli)
    logger.info('supported_languages: %s' % supported_languages)

    logger.info('Creating the frontmatter configuration')
    create_frontmatter_config_file(openapi_file=args.openapi, input_config_file=input_frontmatter_config, supported_languages=supported_languages, output_config_file=output_frontmatter_config)

    logger.info('Calling frontmatter to generate the md file')
    create_frontmatter_md_file(frontmatter_cli=frontmatter_cli, openapi_file=args.openapi, frontmatter_config_file=output_frontmatter_config, output_file=frontmatter_md_file)

    logger.info('Creating language specific middle panel')
    create_language_specific_files(sdk_generator_cli=sdk_generator_cli, supported_languages=supported_languages, openapi_file=args.openapi, output_folder=args.output_folder)

    logger.info('Renaming language-specific files according to apiref-index.json')
    rename_language_specific_files(openapi_file=args.openapi, languages=supported_languages, apidocs=args.apidocs, output_folder=args.output_folder)

def get_basename(filepath):
  '''Returns the basename of the given filepath without the file extension'''

  if not filepath:
    raise ValueError('openapi file path cannot be null or empty')
  basename= os.path.basename(filepath)
  return os.path.splitext(basename)[0]

def get_frontmatter_cli(frontmatter):
  '''Returns the absolute path to the frontmatter app.js file

  Arguments:
    sdk_generator {String} -- The path to the app.js file or the folder where the app.js file is

  Raises:
    ValueError -- if the given path doesn't exist

  Returns:
    String -- The absolute file path to the frontmatter app.js file
  '''

  if not frontmatter:
    raise ValueError('Frontmatter file path cannot be null or empty')

  cli = frontmatter

  if (not os.path.isabs(cli)):
    cli = os.path.abspath(cli)

  if (os.path.isdir(frontmatter)):
      cli = '%s/app.js' % cli

  if (not os.path.exists(cli)):
    raise ValueError('%s is not a valid path' % frontmatter)

  return cli

def get_sdk_generator_cli(sdk_generator):
  '''Returns the absolute path to the Jar file where the SDK Generator is

  Arguments:
    sdk_generator {String} -- The path to the jar file or the folder where the jar file is

  Raises:
    ValueError -- if the given path doesn't exist

  Returns:
    String -- The absolute file path to the SDK Generator jar file
  '''

  if not sdk_generator:
    raise ValueError('SDK Generator file path cannot be null or empty')

  cli = sdk_generator

  if (not os.path.isabs(cli)):
    cli = os.path.abspath(cli)

  if (os.path.isdir(sdk_generator)):
      cli = '%s/openapi-sdkgen.jar' % cli

  if (not os.path.exists(cli)):
    raise ValueError('%s is not a valid path' % sdk_generator)

  return cli

def get_supported_languages(openapi_file=None):
  '''
  Generates the list of supported languages to be used by the SDK generator.
  The list is derived from the x-sdk-supported-languages in the OAS API definition file

  Arguments:
    openapi_file {String} -- The name of the OAS API definition file

  Raises:
    ValueError -- if a required file cannot be found or parsed

  Returns:
    String -- The array of supported languages
  '''

  with open(openapi_file) as f:
    openapi = json.load(f)

  supported_languages = openapi['info']['x-sdk-supported-languages']

  return supported_languages

def get_latest_sdk_version(language):
  '''
  Performs an HTTP GET to retrieve the GitHub release page for the latest
  SDK release for the specified language, and parses the returned HTML to
  find the release number.

  Arguments:
    language {String} -- The name of the SDK language (for example, "java").

  Raises:
    RuntimeError -- If the version number cannot be identified from the page

  Returns:
    String -- The version number (for example, "2.1").
  '''
  url = 'https://github.com/watson-developer-cloud/' + language + '-sdk/releases/latest'
  page = html.fromstring(requests.get(url).content)

  matches = page.xpath(r"//div[@class='release-header'][1]//a[re:match(text(), '^v?[\d.]+$')]",
                        namespaces={"re": "http://exslt.org/regular-expressions"})
  
  if (len(matches) > 0):
    if (matches[0].text[0] == 'v'):
      sdk_ver = matches[0].text[1:]
    else:
      sdk_ver = matches[0].text
  else:
    raise RuntimeError('Latest SDK version for %s not found in expected format' % language)

  return sdk_ver

def create_frontmatter_config_file(openapi_file=None, input_config_file=None, supported_languages=None, output_config_file=None):
  '''
  Generates the config file that will be used for front matter generation.
  Any value specified in the input YAML config will be passed through
  as-is. Other values (if required) are derived from the OAS file or
  queried from GitHub.

  Arguments:
    openapi_file {String} -- The name of the OAS API definition file
    config_file {String} -- The name of the input config YAML file
    supported_languages {String} -- The supported languages from the OAS API definition file
    output_file {String} -- The name of the generated front matter config file

  Raises:
    ValueError -- if a required file cannot be found or parsed

  '''

  with open(input_config_file) as f:
    input_fm_config = json.load(f, object_pairs_hook=OrderedDict)
  with open(openapi_file) as f:
    openapi = json.load(f)

  output_fm_config = OrderedDict(input_fm_config.items())
  if 'serviceMajorVersion' not in output_fm_config:
    output_fm_config['serviceMajorVersion'] = openapi['info']['version'].split('.')[0]

  for l in supported_languages:
    output_fm_config[l+'SdkVersion'] = get_latest_sdk_version(l)

  with open(output_config_file, 'w') as f:
    json.dump(output_fm_config, f, indent=2, separators=(',', ': '))

def create_frontmatter_md_file(frontmatter_cli=None, openapi_file=None, frontmatter_config_file=None, output_file=None):
  '''
  Generates the Markdown source file (md) file from the front matter config file generated
  in the previous step.  Assumes the frontmatter-generator repository has been downloaded and
  is accessible to enable the call to app.js to execute properly.

  Arguments:
    frontmatter_cli {String} -- The name of the frontmatter app.js file
    openapi_file {String} -- The name of the OAS API definition file
    frontmatter_config_file {String} -- The name of the generated front matter config file
    output_file {String} -- The name of the generated md file

  Raises:
    ValueError -- if a required file cannot be found or parsed
  '''

  logger.info('\n')
  logger.info('frontmatter_cli: %s' % frontmatter_cli)
  logger.info('openapi_file: %s' % openapi_file)
  logger.info('frontmatter_config_file: %s' % frontmatter_config_file)
  logger.info('output_file: %s' % output_file)

  fg_command = "node %s -i %s -c %s -o %s" % (frontmatter_cli, openapi_file, frontmatter_config_file, output_file)

#  working_directory = os.path.dirname(frontmatter_cli)
  working_directory = os.path.dirname(frontmatter_cli)
  logger.info('frontmatter generator command: %s' % fg_command)
  logger.info('frontmatter generator location: %s' % working_directory)

  subprocess.call(fg_command, shell=True, cwd=working_directory)

def create_language_specific_files(sdk_generator_cli=None, supported_languages=None, openapi_file=None, output_folder=None):
  '''
  Generates the middle panel for all supported languages.  Assumes the SDK generator (openapi-sdkgen) release directory has been
  downloaded and is accessible to enable the call to openapi-sdkgen.sh to execute properly.

  Arguments:
    sdk_generator_cli {String} -- The name of the sdk generator shell script
    supported_languages {String} -- The supported languages from the OAS API definition file
    openapi_file {String} -- The name of the OAS API definition file
    output_folder {String} -- The name of the folder where the middle column for each language will be written

  Raises:
    ValueError -- if a required file cannot be found or parsed
  '''

  logger.info('\n')
  logger.info('sdk_generator_cli: %s' % sdk_generator_cli)
  logger.info('supported_languages: %s' % supported_languages)
  logger.info('openapi_file: %s' % openapi_file)
  logger.info('output_folder: %s' % output_folder)

  working_directory = os.path.dirname(sdk_generator_cli)
  logger.info('SDK generator location: %s' % working_directory)

  for sdk in supported_languages:
    watson_sdk = 'watson-' + sdk
    sdk_command = "java -jar %s generate -i %s -g %s -o %s" % (sdk_generator_cli, openapi_file, watson_sdk, output_folder)
    logger.info('SDK generator command: %s' % sdk_command)
    subprocess.call(sdk_command, shell=True, cwd=working_directory)

def rename_language_specific_files(openapi_file=None, languages=None, apidocs=None, output_folder=None):
  
  index_file = os.path.join(apidocs, 'apiref-index.json')
  openapi_filename = os.path.basename(openapi_file)

  if not os.path.isfile(index_file):
    logger.warning('apiref-index.json not found. SDK files not renamed.')
    return

  with open(index_file) as f:
    index = json.load(f)
  
  if not openapi_filename in index:
    logger.warning(openapi_filename + ' not defined in apiref-index.json. SDK files not renamed.')
    return

  for lang in languages:
    old_file = os.path.join(output_folder, lang + '-apiref.json')
    if os.path.isfile(old_file):
      if lang in index[openapi_filename]:
        new_file = os.path.join(output_folder, index[openapi_filename][lang])
        if os.path.isfile(new_file):
          os.remove(new_file)
        os.rename(old_file, new_file)
      else:
        logger.warning('SDK file for ' + lang + ' not defined in apiref-index.json. File not renamed.')
        logger.warning(lang + ' = ' + index[openapi_filename][lang])
    else:
      logger.warning(lang + '-apiref.json not found.')
        
  return
