import requests
import json
from collections import namedtuple
requests.packages.urllib3.disable_warnings()

AccountResponse = namedtuple('AccountResponse', [
    'fullName',
    "id",
    "isActive",
    "isAdmin",
    "isImported",
    "isOrg",
    "membersCount",
    "name"
])

AccountRequest = namedtuple('AccountRequest', [
    "fullName",
    "isActive",
    "isAdmin",
    "isOrg",
    "name",
    "password",
    "searchLDAP"
])

TeamResponse = namedtuple('TeamResponse', [
    "description",
    "id",
    "membersCount",
    "name",
    "orgID"
])

TeamRequest = namedtuple('TeamRequest', [
    "description",
    "name"
])

TeamMemberRequest = namedtuple('TeamMemberRequest', [
    "orgNameOrID",
    "teamNameOrID",
    "memberNameOrID",
    "isAdmin"
])


# List users or organizations
def get_accounts(
    base_url,
    auth_token,
    account_type_filter,
    timeout=5
):
    """List users
     
    base_url (string):
        Base URL to ucp server
    timeout(int):
        Timeout in seconds
    filter(string):
        Filter account by type: users, orgs, admins, active-users, inactive-users, all
    Returns:
        list of users
    """

    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            base_url + '/accounts/?filter=' + account_type_filter,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text
    
    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)

# List members of an organization
def get_org_members(
    base_url,
    auth_token,
    orgNameOrID,
    timeout=5
):
    """List members of an organization

    base_url (string):
        Base URL to ucp server
    timeout(int):
        Timeout in seconds
    Returns:
        list of users
    """

    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            base_url + '/accounts/' +  orgNameOrID + '/members',
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text
    
    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


# List users or organizations
def get_account_details(
    base_url,
    auth_token,
    accountNameOrId,
    timeout=5
):
    """Get account details
    
    base_url (string):
        Base URL to ucp server
    timeout(int):
        Timeout in seconds
    Returns:
        list of users
    """

    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            base_url + '/accounts/' +  accountNameOrId,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text
    
    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)

# List teams in an organizations
def get_teams(
    base_url,
    auth_token,
    orgname,
    timeout=5
):
    """List teams in an organization
     
    base_url (string):
        Base URL to ucp server
    timeout(int):
        Timeout in seconds
    Returns:
        list of teams in an organization
    """

    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            base_url + '/accounts/' + orgname + '/teams',
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text
    
    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


def get_team(
    base_url,
    auth_token,
    orgNameOrID,
    teamNameOrID,
    timeout=5
):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            base_url + '/accounts/' + orgNameOrID + '/teams/' + teamNameOrID,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.json()

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)

# Create user or organization
# POST /accounts
def create_account(
    base_url,
    auth_token,
    account_request,
    timeout=5
):
    """Create user or organization
     
    base_url (string):
        Base URL to ucp server
    timeout(int):
        Timeout in seconds
    Returns:
        something (string)
    """

    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    payload = {
         "fullName": account_request.fullName,
         "isActive": account_request.isActive,
         "isAdmin":  account_request.isAdmin,
         "isOrg":    account_request.isOrg,
         "name":     account_request.name,
         "password": account_request.password,
         "searchLDAP": account_request.searchLDAP
    }
 
    try:
        response = requests.post(
            base_url + '/accounts/',
            json=payload,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.json()
    
    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


def delete_account(
    base_url,
    auth_token,
    accountNameOrId,
    timeout=5
):
    """Delete a user or organization account
     
    base_url (string):
        Base URL to ucp server
    timeout(int):
        Timeout in seconds
    accountNameOrId:
        Account or organization name
    Returns:
        something (string)
    """

    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }
 
    try:
        response = requests.delete(
            base_url + '/accounts/' + accountNameOrId,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text
    
    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        print(e.response.status_code)
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)

# Create a team
# POST /accounts/{orgNameOrID}/teams
def create_team(
    base_url,
    auth_token,
    timeout,
    team_request,
    name,
    org
):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    payload = {
         "description": team_request.description,
         "name": team_request.name
    }

    try:
 
        response = requests.post(
            base_url + '/accounts/' + org + "/teams",
            json=payload,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        data = response.json()
        return data

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)

def delete_team(
    base_url,
    auth_token,
    orgNameOrId,
    teamNameOrId,
    timeout=5
):
    """Delete a user or organization account

    base_url (string):
        Base URL to ucp server
    timeout(int):
        Timeout in seconds
    orgNameOrId:
        Organization name or id
    Returns:
        something (string)
    """

    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }
 
    try:
        response = requests.delete(
            base_url + '/accounts/' + orgNameOrId + '/teams/' + teamNameOrId ,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text
    
    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:

        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


def get_team_member_details(
    base_url,
    auth_token,
    orgNameOrID,
    teamNameOrID,
    memberNameOrID,
    timeout    
):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            base_url + '/accounts/' + orgNameOrID + '/teams/' + teamNameOrID + '/members/' + memberNameOrID,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:

        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


 
def get_team_members(
    base_url,
    auth_token,
    orgNameOrID,
    teamNameOrID,
    timeout    
):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(
            base_url + '/accounts/' + orgNameOrID + '/teams/' + teamNameOrID + '/members',
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:

        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


def add_team_member(
    base_url,
    auth_token,
    orgNameOrID,
    teamNameOrID,
    memberNameOrID,
    timeout    
):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    payload = {
        "isAdmin": False
    }

    try:
        response = requests.put(
            base_url + '/accounts/' + orgNameOrID + '/teams/' + teamNameOrID + '/members/' + memberNameOrID,
            json=payload,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


def remove_team_member(
    base_url,
    auth_token,
    orgNameOrID,
    teamNameOrID,
    memberNameOrID,
    timeout=5
):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.delete(
            base_url + '/accounts/' + orgNameOrID + '/teams/' + teamNameOrID + '/members/' + memberNameOrID,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)


def remove_org_member(
    base_url,
    auth_token,
    orgNameOrID,
    memberNameOrID,
    timeout=5
):
    headers = {
        'Authorization': "Bearer " + auth_token,
        'Content-Type': 'application/json'
    }

    try:
        response = requests.delete(
            base_url + '/accounts/' + orgNameOrID + '/members/' + memberNameOrID,
            timeout=timeout,
            verify=False,
            headers=headers
        )
        response.raise_for_status()
        return response.text

    except (requests.ConnectionError, requests.Timeout) as e:
        raise errors.Unavailable() from e

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400 or e.response.status_code == 404:
            errors = e.response.json()
            error = errors['errors'][0]
            code = error['code']
            message = error['message']
            print(message)

