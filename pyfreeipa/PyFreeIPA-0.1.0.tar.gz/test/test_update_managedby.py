"""
A generic wrapper script for the pyfreeipa Api class
"""
import json
import sys
from datetime import datetime
from pyfreeipa.Api import Api
from pyfreeipa.configuration import CONFIG


def main():
    """
    @brief      This provides a wrapper for the pyfreeipa module

    @return     { description_of_the_return_value }
    """
    startTime = datetime.now()
    updates = 0
    unchanged = 0

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

    tokens = ipaapi.otptokens(CONFIG['uid'])

    for token in tokens:
        token_managers = []
        if CONFIG['otptoken']['managedby']:
            token_managers = list(CONFIG['otptoken']['managedby'])
        if 'ipatokenowner' in token:
            if CONFIG['otptoken']['ownermanagedby']:
                token_managers.append(token['ipatokenowner'][0])

        addmanagedby = []
        removemanagedby = []
        currentmanagers = []

        if 'managedby_user' in token:
            currentmanagers = token['managedby_user']
            for manager in token_managers:
                if manager:
                    if manager not in token['managedby_user']:
                        addmanagedby.append(manager)

            for manager in token['managedby_user']:
                if manager:
                    if manager not in token_managers:
                        removemanagedby.append(manager)

        else:
            addmanagedby = token_managers

        if CONFIG['dryrun']:
            print(
                "Token: %s Current: %s Proposed: %s Add: %s Remove: %s" %
                (
                    token['ipatokenuniqueid'][0],
                    currentmanagers,
                    token_managers,
                    addmanagedby,
                    removemanagedby
                )
            )

        if addmanagedby:
            addresponse = ipaapi.otptoken_add_managedby(
                token['ipatokenuniqueid'][0],
                user=addmanagedby
            )
            if CONFIG['dryrun']:
                print("DRY RUN")
                prettyprintpost(addresponse)
            else:
                if addresponse.json()['error']:
                    print(
                        "ERROR: Failed to update %s" %
                        token['ipatokenuniqueid'][0]
                    )
                    print(
                        json.dumps(
                            addresponse.json(),
                            indent=4,
                            sort_keys=True
                        )
                    )
                else:
                    print(
                        "DONE: %s added %s" %
                        (
                            token['ipatokenuniqueid'][0],
                            addmanagedby
                        )
                    )

        if removemanagedby:
            removeresponse = ipaapi.otptoken_remove_managedby(
                token['ipatokenuniqueid'][0],
                user=removemanagedby
            )
            if CONFIG['dryrun']:
                print("DRY RUN")
                prettyprintpost(removeresponse)
            else:
                if removeresponse.json()['error']:
                    print(
                        "ERROR: Failed to update %s" %
                        token['ipatokenuniqueid'][0]
                    )
                    print(
                        json.dumps(
                            removeresponse.json(),
                            indent=4,
                            sort_keys=True
                        )
                    )
                else:
                    print(
                        "DONE: %s removeded %s" %
                        (
                            token['ipatokenuniqueid'][0],
                            removemanagedby
                        )
                    )

        if removemanagedby or addmanagedby:
            updates += 1
        else:
            unchanged += 1

    print("Total tokens: %s" % len(tokens))
    print("Token updates: %s" % updates)
    print("Tokens unchanged: %s" % unchanged)

    deltatime = datetime.now() - startTime
    print("Elapsed time: %s" % str(deltatime))


def prettyprintpost(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in
    this function because it is programmed to be pretty
    printed and may differ from the actual request.
    Brutally copypasted from: https://stackoverflow.com/a/23816211
    """
    jsonbody = json.loads(req.body)
    body = json.dumps(jsonbody, indent=4, sort_keys=True)
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        body
    ))


if __name__ == "__main__":
    main()
