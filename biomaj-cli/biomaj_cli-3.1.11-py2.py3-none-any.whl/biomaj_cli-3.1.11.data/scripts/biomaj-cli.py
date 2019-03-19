#!python
import os
import sys
import argparse
import logging
import getpass
import requests
import datetime
import json

from biomaj_cli.utils import Utils
from biomaj_cli.utils import Options
from biomaj_core.config import BiomajConfig


def main():

    parser = argparse.ArgumentParser(add_help=False)
    Utils.set_args(parser)

    options = Options()
    parser.parse_args(namespace=options)

    options.no_log = False

    if options.help:
        print('''
    --config: global.properties file path (local install only)

    --proxy: BioMAJ daemon url (http://x.y.z)

    --trace: Trace workflow in Zipkin server

    --api-key: User API key to authenticate against proxy

    --whatsup: Get info on what biomaj is doing

    --last-log: Get log file of last session
        [MANDATORY]
        --proxy http://x.y.z
        [OPTIONAL]
        --tail X number of lines to tail from log file

    --about-me: Get my info
        [MANDATORY]
        --proxy http://x.y.z
        --user-login XX
        --user-password XX

    --update-status: get status of an update
        [MANDATORY]
        --bank xx: name of the bank to check
        --proxy http://x.y.z

    --update-cancel: cancel current update
        [MANDATORY]
        --bank xx: name of the bank to cancel
        --proxy http://x.y.z

    --status: list of banks with published release
        [OPTIONAL]
        --bank xx / bank: Get status details of bank

    --status-ko: list of banks in error status (last run)

    --log DEBUG|INFO|WARN|ERR  [OPTIONAL]: set log level in logs for this run, default is set in global.properties file

    --check: Check bank property file
        [MANDATORY]
        --bank xx: name of the bank to check (will check xx.properties)

    --owner yy: Change owner of the bank (user id)
        [MANDATORY]
        --bank xx: name of the bank

    --visibility public|private: change visibility public/private of a bank
        [MANDATORY]
        --bank xx: name of the bank

    --change-dbname yy: Change name of the bank to this new name
        [MANDATORY]
        --bank xx: current name of the bank

    --move-production-directories yy: Change bank production directories location to this new path, path must exists
        [MANDATORY]
        --bank xx: current name of the bank

    --update: Update bank
        [MANDATORY]
        --bank xx: name of the bank(s) to update, comma separated
        [OPTIONAL]
        --publish: after update set as *current* version
        --from-scratch: force a new update cycle, even if release is identical, release will be incremented like (myrel_1)
        --stop-before xx: stop update cycle before the start of step xx
        --stop-after xx: stop update cycle after step xx has completed
        --from-task xx --release yy: Force an re-update cycle for bank release *yy* or from current cycle (in production directories), skipping steps up to *xx*
        --process xx: linked to from-task, optionally specify a block, meta or process name to start from
        --release xx: release to update

    --publish: Publish bank as current release to use
        [MANDATORY]
        --bank xx: name of the bank to update
        --release xx: release of the bank to publish

    --unpublish: Unpublish bank (remove current)
        [MANDATORY]
        --bank xx: name of the bank to update

    --remove-all: Remove all bank releases and database records
        [MANDATORY]
        --bank xx: name of the bank to update
        [OPTIONAL]
        --force: remove freezed releases

    --remove-pending: Remove pending releases
        [MANDATORY]
        --bank xx: name of the bank to update

    --remove: Remove bank release (files and database release)
        [MANDATORY]
        --bank xx: name of the bank to update
        --release xx: release of the bank to remove

        Release must not be the *current* version. If this is the case, publish a new release before.

    --freeze: Freeze bank release (cannot be removed)
        [MANDATORY]
        --bank xx: name of the bank to update
        --release xx: release of the bank to remove

    --unfreeze: Unfreeze bank release (can be removed)
        [MANDATORY]
        --bank xx: name of the bank to update
        --release xx: release of the bank to remove

    --search: basic search in bank production releases, return list of banks
       --formats xx,yy : list of comma separated format
      AND/OR
       --types xx,yy : list of comma separated type

       --query "LUCENE query syntax": search in index (if activated)

    --show: Show bank files per format
      [MANDATORY]
      --bank xx: name of the bank to show
      [OPTIONAL]
      --release xx: release of the bank to show

    --maintenance on/off/status: (un)set biomaj in maintenance mode to prevent updates/removal

    --schedule: Get bank scheduling (needs biomaj-release)
        [MANDATORY]
        --proxy http://x.y.z

    --history: Get biomaj update/remove history
        [OPTIONAL]
        --history-limit xx : number of elements to return

    --stats: Get statistics

    --json: Get output in JSON format

    --data-list: List available bank templates
      [MANDATORY]
      biomaj-data package

    --data-import: Import a bank template
      [MANDATORY]
      biomaj-data package
      --bank xx : template name
        ''')

        return

    proxy = options.proxy

    if 'BIOMAJ_PROXY' in os.environ:
        proxy = os.environ['BIOMAJ_PROXY']
        options.proxy = proxy

    if 'BIOMAJ_APIKEY' in os.environ:
        apikey = os.environ['BIOMAJ_APIKEY']
        options.apikey = apikey

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)

    if not proxy:
        try:
            from biomaj_daemon.daemon.utils import biomaj_client_action
        except Exception as e:
            print('Failed to import biomaj libraries. Either you forgot the --proxy option, either you use a local biomaj install and did not installed it (biomaj-daemon package)')

    try:
        if not proxy:
            from biomaj_daemon.daemon.utils import biomaj_client_action
            options.user = getpass.getuser()
            BiomajConfig.load_config(options.config)
            status = False
            msg = None
            try:
                (status, msg) = biomaj_client_action(options)
            except Exception as e:
                status = False
                msg = str(e)
        else:
            headers = {}
            if options.apikey:
                headers = {'Authorization': 'APIKEY ' + options.apikey}

            if options.schedule:
                r = requests.get(proxy + '/api/release/schedule', headers=headers)
                if not r.status_code == 200:
                    print('Failed to contact schedule service')
                    sys.exit(1)
                schedule = r.json()
                for bank in schedule['schedule']:
                    sched_next = 'not planned'
                    if bank['next'] is not None:
                        sched_next = datetime.datetime.fromtimestamp(bank['next'])
                    print(bank['name'] + ': ' + str(sched_next))
                sys.exit(0)

            if options.lastlog:
                if not options.bank:
                    print("--bank is missing\n")
                    sys.exit(1)
                if options.tail:
                    r = requests.get(proxy + '/api/daemon/bank/' + options.bank + '/log/' + options.tail, headers=headers)
                    print(r.text)
                else:
                    r = requests.get(proxy + '/api/daemon/bank/' + options.bank + '/log', headers=headers)
                    print(r.text)
                sys.exit(0)

            r = requests.post(proxy + '/api/daemon', headers=headers, json={'options': options.__dict__})
            if not r.status_code == 200:
                print('Failed to contact BioMAJ daemon')
                sys.exit(1)
            result = r.json()
            status = result['status']
            msg = result['msg']

        if options.json:
            if not status:
                print(json.dumps({'error': str(msg)}))
            else:
                print(json.dumps(msg))
        else:
            if not status:
                print('An error occured:\n')
                print(str(msg))
            else:
                if msg:
                    print(str(msg))
                else:
                    print('Done.')
    except Exception as e:
        logging.exception(e)
        print('Error:' + str(e))

if __name__ == '__main__':
    main()
