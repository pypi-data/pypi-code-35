import click
import getpass
from .common import common_options, pass_state
from .config import Config
from apis import auth as auth_api

# login
@click.command('login')
@common_options
@pass_state
@click.option('username', '-u','--username', help='username', required=True)
@click.option('password', '-p','--password', help='password', required=False)
@click.option('url', '--url', help='ucp url', required=True)
def login(state, username, password, url):
    config = Config()
    verify_tls = False

    if password == None:
        password = getpass.getpass('Password: ')

    config.set_username(username)
    config.set_url(url)

    login_response = auth_api.login(url, username, password, 5, verify_tls)
    if login_response == None:
        return
    else:
        print("Login Succeeded")

    auth_token = login_response.auth_token
    config.set_authtoken(auth_token)

    bundle_file = auth_api.clientbundle(url, auth_token, 5, verify_tls)
    config.save_bundle_file(bundle_file)
    config.extract_bundle_file()

# eval
@click.command('env')
def env():
    click.echo('pushd $(pwd) && cd ~/.ucp/bundle && eval "$(<env.sh)" && popd')
 