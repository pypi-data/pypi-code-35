"""
A generic wrapper script for the pyfreeipa Api class
"""
import json
import sys
import datetime
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
        users = ipaapi.users(
            uid=CONFIG['uid'],
            in_group=CONFIG['group']
        )
    elif CONFIG['uid']:
        users = ipaapi.users(CONFIG['uid'])
    elif CONFIG['group']:
        users = ipaapi.users(in_group=CONFIG['group'])
    else:
        users = ipaapi.users()

    today = datetime.date.today()
    margin = datetime.timedelta(days=7)
    inaweek = today + margin
    timeformat = '%Y%m%d%H%M%SZ'
    expiringusers = []

    for user in users:
        if 'krbpasswordexpiration' in user:
            expiry = datetime.datetime.strptime(
                user['krbpasswordexpiration'][0]['__datetime__'],
                timeformat
            )
            if isinstance(expiry, datetime.datetime):
                if today <= expiry.date() <= inaweek:
                    expiringusers.append(user['uid'][0])

    print("Users with passwords expiring this week: %s" % expiringusers)


if __name__ == "__main__":
    main()
