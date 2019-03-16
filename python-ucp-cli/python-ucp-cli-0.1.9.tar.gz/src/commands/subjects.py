import click
import json
import sys
from .config import Config
from apis import accounts as accounts_api

pass_config = click.make_pass_decorator(Config, ensure=True)

#
# Organization
#
@click.group()
def org():
    pass

# org list
@click.command('list')
@pass_config
def list_orgs(config):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    response_text = accounts_api.get_accounts(base_url, auth_token, 'orgs')
    print(response_text)

org.add_command(list_orgs)


# org show
@click.command('show')
@click.option('name', '--name', help='username', required=True)
@pass_config
def show_org(config, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.get_account_details(base_url, auth_token, name)
    if result != None:
        click.echo(result)

org.add_command(show_org)

# org create
@click.command('create')
@click.option('name', '--name', help='organization name', required=True)
@pass_config
def create_org(config, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()

    account_request = accounts_api.AccountRequest(
        fullName=None,
        isActive=True,
        isAdmin=False,
        isOrg=True,
        name=name,
        password=None,
        searchLDAP=False
    )
    accounts_api.create_account(base_url, auth_token, account_request)

org.add_command(create_org)

# org delete
@click.command('delete')
@click.option('name', '--name', help='organization name', required=True)
@pass_config
def delete_org(config, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    accounts_api.delete_account(base_url, auth_token, name)
    
org.add_command(delete_org)

#
# Org members
#
# org member
# 
@click.group('member')
def org_member():
    pass


# org member list
@click.command('list')
@click.option('org', '--org', help='organization', required=True)
@pass_config
def org_member_list(config, org):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.get_org_members(base_url, auth_token, org, 5)
    click.echo(result)

org_member.add_command(org_member_list)

# org member remove
@click.command('remove')
@click.option('org', '--org', help='organization', required=True)
@click.option('name', '--name', help='name', required=True)
@pass_config
def org_member_remove(config, org, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.remove_org_member(base_url, auth_token, org, name, 5)
    click.echo(result)

org_member.add_command(org_member_remove)

org.add_command(org_member)


#
# Teams
#

# team sub-commands
@click.group()
def team():
    pass

# team create
@click.command('create')
@click.option('name', '--name', help='team name', required=True)
@click.option('org', '--org', help='organization ', required=True)
@click.option('description', '--description', help='team description', required=False)
@pass_config
def create_team(config, name, org, description):
    base_url = config.get_url()
    auth_token = config.get_authtoken()

    team_request = accounts_api.TeamRequest(
        description=description,
        name=name
    )
    accounts_api.create_team(base_url, auth_token, 5, team_request, name, org)
 
team.add_command(create_team)


# team delete
@click.command('delete')
@click.option('name', '--name', help='team name', required=True)
@click.option('org', '--org', help='organization ', required=True)
@pass_config
def delete_team(config, name, org):
    base_url = config.get_url()
    auth_token = config.get_authtoken()

    result = accounts_api.delete_team(base_url, auth_token, org, name, 5)
    if result != None:
        click.echo(result)
 
team.add_command(delete_team)

# team list
@click.command('list')
@click.option('org', '--org', help='organization ', required=True)
@pass_config
def list_teams(config, org):
    base_url = config.get_url()
    auth_token = config.get_authtoken()

    result = accounts_api.get_teams(base_url, auth_token, org, 5)
    click.echo(result)

team.add_command(list_teams)

# team show
@click.command('show')
@click.option('org', '--org', help='organization', required=True)
@click.option('name', '--name', help='name', required=True)
@pass_config
def show_team(config, org, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.get_team(base_url, auth_token, org, name, 5)
    click.echo(result)

team.add_command(show_team)

# team member sub-commands
@click.group('member')
def team_member():
    pass

# team member list
@click.command('list')
@click.option('team', '--team', help='team', required=True)
@click.option('org', '--org', help='organization', required=True)
@pass_config
def team_member_list(config, team, org):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.get_team_members(base_url, auth_token, org, team, 5)
    click.echo(result)

team_member.add_command(team_member_list)


# team member show
@click.command('show')
@click.option('name', '--name', help='name', required=True)
@click.option('team', '--team', help='team', required=True)
@click.option('org', '--org', help='organization', required=True)
@pass_config
def team_member_show(config, name, team, org):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.get_team_member_details(base_url, auth_token, org, team, name, 5)
    click.echo(result)

team_member.add_command(team_member_show)

# team member add
@click.command('add')
@click.option('name', '--name', help='name', required=True)
@click.option('team', '--team', help='team', required=True)
@click.option('org', '--org', help='organization', required=True)
@pass_config
def team_member_add(config, name, team, org):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.add_team_member(base_url, auth_token, org, team, name, 5)
    click.echo(result)

team_member.add_command(team_member_add)

# team member remove
@click.command('remove')
@click.option('name', '--name', help='name', required=True)
@click.option('team', '--team', help='team', required=True)
@click.option('org', '--org', help='organization', required=True)
@pass_config
def team_member_remove(config, org, team, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.remove_team_member(base_url, auth_token, org, team, name, 5)
    click.echo(result)

team_member.add_command(team_member_remove)

team.add_command(team_member)

#
# Users
#
# user sub-command
@click.group()
def user():
    pass

# user list
@click.command('list')
@pass_config
def list_users(config):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.get_accounts(base_url, auth_token, 'users')
    if result != None:
        click.echo(result)
    
user.add_command(list_users)

# user show
@click.command('show')
@click.option('name', '--name', help='username', required=True)
@pass_config
def show_user(config, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    result = accounts_api.get_account_details(base_url, auth_token, name)
    if result != None:
        click.echo(result)

user.add_command(show_user)

# user create
@click.command('create')
@click.option('name', '--name', help='username', required=True)
@click.option('password', '--password', help='password', required=True)
@pass_config
def create_user(config,name, password):
    base_url = config.get_url()
    auth_token = config.get_authtoken()

    account_request = accounts_api.AccountRequest(
        fullName=None,
        isActive=True,
        isAdmin=False,
        isOrg=False,
        name=name,
        password=password,
        searchLDAP=False
    )
    accounts_api.create_account(base_url, auth_token, account_request)

user.add_command(create_user)

# user delete
@click.command('delete')
@click.option('name', '--name', help='username', required=True)
@pass_config
def delete_user(config, name):
    base_url = config.get_url()
    auth_token = config.get_authtoken()
    accounts_api.delete_account(base_url, auth_token, name)

user.add_command(delete_user)
