'''

Copyright (C) 2019 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

The watcher is actually a connection to crontab. This is what helps to schedule
the watched to check for changes at some frequency, and update the files.

'''

from crontab import CronTab


def schedule_watcher(user=None):
    '''schedule the watcher to run at some frequency to update record of pages.
    '''
    # If no user provided, just default to running user
    if user == None:
        user = True

    cron = CronTab(user=True, tab="* * * * * watchme run")
    return cron
