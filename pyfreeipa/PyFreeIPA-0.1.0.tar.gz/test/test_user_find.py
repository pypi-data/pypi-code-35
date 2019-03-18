"""
A generic wrapper script for the pyfreeipa Api class
"""
import json
import sys
from pyfreeipa.Api import Api
from pyfreeipa.configuration import CONFIG


def main():
    """
    @brief      This provides a wrapper for the pyfreeipa module

    @return     { description_of_the_return_value }
    """

    if CONFIG['command'] == 'dumpconfig':
        print(json.dumps(CONFIG, indent=4, sort_keys=True))
        sys.exit(0)

    # Define API session
    ipaapi = Api(
        host=CONFIG['ipaserver']['host'],
        username=CONFIG['ipaserver']['user'],
        password=CONFIG['ipaserver']['password'],
        port=CONFIG['ipaserver']['port'],
        verify_ssl=CONFIG['ipaserver']['verify_ssl'],
        verify_method=CONFIG['ipaserver']['verify_method'],
        verify_warnings=CONFIG['ipaserver']['verify_warnings'],
        dryrun=CONFIG['dryrun']
    )

    if CONFIG['uid'] and CONFIG['group']:
        response = ipaapi.user_find(
            uid=CONFIG['uid'],
            in_group=CONFIG['group']
        )
        users = ipaapi.users(
            uid=CONFIG['uid'],
            in_group=CONFIG['group']
        )
    elif CONFIG['uid']:
        response = ipaapi.user_find(
            CONFIG['uid']
        )
        users = ipaapi.users(CONFIG['uid'])
    elif CONFIG['group']:
        response = ipaapi.user_find(
            in_group=CONFIG['group']
        )
        users = ipaapi.users(in_group=CONFIG['group'])
    else:
        response = ipaapi.user_find()
        users = ipaapi.users()

    print("The request")
    print(response.request.body)

    print("Raw response:")
    print(json.dumps(response.json(), indent=4, sort_keys=True))

    print("Response as a list object:")
    print(json.dumps(users, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
