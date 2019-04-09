import click
import requests
#import yaml
import json
import time

from requests.auth import HTTPBasicAuth

#with open("config.yml", 'r') as config_file:
#    config = yaml.safe_load(config_file);

#response = requests.get('https://api.testery.io/api/users/me', auth=HTTPBasicAuth(config['username'], config['password']))

#print(response.json())

# @click.argument('create-test-run')

#def post_api(endpoint):
#    requests.post('https://api.testery.io/api' + endpoint)


headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
api_base_url = 'https://api.dev.testery.io/api'


def api_wait_testrun(username, token, test_run_id, output):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    test_run = requests.get(api_base_url + '/test-run-results/' + str(test_run_id), auth=HTTPBasicAuth(username, token), headers=headers).json()

    while test_run['status'] not in ['PASS','FAIL']:

        test_run = requests.get(api_base_url + '/test-run-results/' + str(test_run_id), auth=HTTPBasicAuth(username, token), headers=headers).json()
        print(test_run)
        time.sleep(1);

    print(test_run)


@click.group()
def cli():
    """
    Testery Command Line Interface\n
    Kick off test runs from your CI/CD platform and run them on Testery's next-generation, cloud-based testing grid.
    """
    pass

@click.command('verify-token')
@click.option('--username', help='Your Testery username.')
@click.option('--token', help='Your Testery API token.')
def verify_token(username, token):
    """
    Verifies your username and authentication token are valid.
    """

    response = requests.get(api_base_url + '/users/me', auth=HTTPBasicAuth(username, token))

    print(response.json())

@click.command('create-test-run')
@click.option('--username', help='Your Testery username.')
@click.option('--token', help='Your Testery API token.')
@click.option('--git-org', help='Your git organization name.')
@click.option('--git-repo', help='Your git repository name.')
@click.option('--git-ref', help='The git commit hash of the build being tested.')
@click.option('--wait-for-results', help='If set, the command will poll until the test run is complete.')
@click.option('--project', help='A unique identifier for your project.')
@click.option('--environment', help='Which environment you would like to run your tests against.')
@click.option('--build-id', help='A unique identifier that identifies this build in your system.')
@click.option('--output', default='json', help='The format for outputting results [json,pretty,teamcity,appveyor]')
def create_test_run(username, token, git_org, git_repo, git_ref, wait_for_results, output, project, environment, build_id):
    """
    Submits a Git-based test run to the Testery platform.
    """
    click.echo("username: %s" % username)
    click.echo("token: %s" % token)
    click.echo("organization: %s" % git_org)
    click.echo("git_repository: %s" % git_repo)
    click.echo("git_ref: %s" % git_ref)
    click.echo("wait_for_results: %s" % wait_for_results)
    click.echo("output: %s" % output)

    test_run_request = {"owner":git_org, "repository":git_repo, "ref":git_ref, "project":project, "environment":environment, "buildId":build_id}



    test_run = requests.post(api_base_url + '/test-run-requests-build',
         auth=HTTPBasicAuth(username, token),
         headers=headers,
         json=test_run_request).json()

    print(test_run)

    test_run_id = str(test_run['id'])

    click.echo("test_run_id: %s" %test_run_id)

    api_wait_testrun(username, token, test_run_id, output)


@click.command('monitor-test-run')
@click.option('--username', help='Your Testery username.')
@click.option('--token', help='Your Testery API token.')
@click.option('--test-run-id', help='The ID for the test run you would like to monitor and wait for.')
@click.option('--output', default='json', help='The format for outputting results [json,pretty,teamcity,appveyor]')
def monitor_test_run(username, token, test_run_id, output):
    api_wait_testrun(username, token, test_run_id, output)

cli.add_command(create_test_run)
cli.add_command(monitor_test_run)
cli.add_command(verify_token)

#if __name__ == '__main__':
#    cli()