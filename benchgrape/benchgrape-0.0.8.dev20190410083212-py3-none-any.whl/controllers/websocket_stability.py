from cement import Controller, ex
from locust.clients import HttpSession
from cement import fs
from benchgrape.core.db import TestDataMapper, RuntimeConfigMapper
from benchgrape.core.statement import login
import os
import subprocess


class Stability(Controller):
    class Meta:
        label = 'websocket'
        stacked_type = 'nested'
        stacked_on = 'base'

    @ex(help='establishes n connections to the server and make a long-running '
             'stability test of the websocket. log everything that seems '
             'unusual. can help a lot when debugging connection issues. '
             'WARNING: THIS DROPS ALL EXISTING BENCHMARK USERS!',
        arguments=[
            (
                    ['--url'], {
                        'help': 'url, example: http://chatgrape.com/',
                        'action': 'store',
                        'required': True
                    }
            ),
            (
                    ['--username'], {
                        'help': 'email/username used for login',
                        'action': 'store',
                        'required': True
                    }
            ),
            (
                    ['--password'], {
                        'help': 'password used for login. hint: 2fa is not '
                                'supported by this program. make sure you '
                                'either disable 2fa temporarily, or, create a '
                                'guest user for this test.',
                        'action': 'store',
                        'required': True
                    }
            ),
            (
                    ['--port'], {
                        'help': 'port to connect to, defaults to 443',
                        'action': 'store',
                        'default': '443'
                    }
            ),
            (
                    ['-n', '--number'], {
                        'help': 'number of websockets to connect, default 10',
                        'action': 'store',
                        'default': '10'
                    }
            ),
            (
                    ['-t', '--duration'], {
                        'help': 'duration of the benchmark in seconds',
                        'action': 'store',
                        'default': '3600'
                    }
            ),
            (
                    ['--logpath'], {
                        'help': 'Path to for files. '
                                'If not set, log will go to stdout/stderr',
                        'action': 'store',
                        'default': './logs'
                    }
            ),
        ],
    )
    def test(self):
        n_ws = self.app.pargs.number
        url = self.app.pargs.url
        username = self.app.pargs.username
        password = self.app.pargs.password
        duration = self.app.pargs.duration
        port = self.app.pargs.port
        logpath = fs.abspath(self.app.pargs.logpath)

        self.app.log.debug('creating log directory and log files.')
        fs.ensure_parent_dir_exists(logpath)
        fs.ensure_dir_exists(logpath)
        debug_fname = fs.join(logpath, 'debug.log')
        stats_fname = fs.join(logpath, 'stats.log')
        open(debug_fname, 'a').close()
        open(stats_fname, 'a').close()

        self.app.log.info('establish %s websocket connections to server %s '
                          'with user %s. press crtl+c to stop the test.' %
                          (n_ws, url, username))

        runtime_config = RuntimeConfigMapper(self.app.db, self.app.log)
        # make sure we always get the same user from the user backend by
        # enabling recycling and only have one user.
        runtime_config.enable_user_recycliing()

        mapper = TestDataMapper(self.app.db, self.app.log)
        self.app.log.info(
            'logging in...'
        )
        token = login(HttpSession(base_url=url), username, password)
        if not token:
            raise RuntimeError(
                f'login at {url} failed. stopping, wont connect to websocket.'
            )
        self.app.log.info(
            'login successful. dropping all existing benchmark users to have '
            'a unique user to test with.'
        )
        mapper.drop_db()
        mapper.init_db()
        # int(u['id']), u['username'], u['password'], u['token']
        mapper.sync_db(
            {
                'id': 0, 'url': url, 'name': '', 'subdomain': ''
             }, [{
                'id': 0, 'username': username, 'password': password,
                'token': token
            }], [], []
        )
        self.app.log.info(
            'successfully added the test user, starting locust. '
            'visit the URL in the browser which will be displayed below '
            'in a few seconds.'
        )

        # subprocess.run([
        #     "locust",
        #     "--locustfile=./benchgrape/locust/locustfiles/stability.py",
        #     f"--host={url}", f"-c={n_ws}", f"-t={duration}", f"-P={port}",
        #     f"--logfile={fs.abspath(stats_fname)}"
        # ])

        locust_file = fs.abspath('./benchgrape/locust/locustfiles/stability.py')
        # todo, this is a dirty hack, find method to locate this file better.
        locust_file = './lib/python3.6/site-packages/benchgrape/locust/locustfiles/stability.py'
        self.app.log.info(f'using locustfile {locust_file}')
        assert os.path.isfile(locust_file), f"locust file {locust_file} does not exist."

        subprocess.run([
            "locust",
            f"--locustfile={locust_file}",
            f"--host={url}",
            # f"--logfile={fs.abspath(stats_fname)}",
        ])
