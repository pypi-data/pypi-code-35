import yaml
import shutil
import bottle
import tarfile
import argparse
from subprocess import call


def main():
    desc = 'Super Simple Auto Deploy bot'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('config_file', action='store',
                        help='The config file for deployments')
    parser.add_argument('-p', '--port', action='store',
                        default='8764',
                        help='Port to run server on')
    parser.add_argument('-i', '--interface', action='store',
                        default='127.0.0.1',
                        help='Host to run server on')
    parser.add_argument('-v', '--verbose', action='store_true',
                        default=False,
                        help='Print out details of web requests?')
    parser.add_argument('--deploy_path', action='store', default='/home/ubuntu', help='Where to put the deployment files?')
    parser.add_argument('--temp_path', action='store', default='/tmp/pullboy_build.tar', help='Where to put the tar file temporarily?')
    parser.add_argument('--deploy_secret', action='store', help='The secret to use for deployment')
    args = parser.parse_args()

    def log(*a, **kw):
        if args.verbose:
            print(*a, **kw)

    bottle.BaseRequest.MEMFILE_MAX = 1024**3  # bytes
    app = bottle.Bottle()

    @app.route('/deploy', method=['POST'])
    def copy_and_unzip():
        secret = bottle.request.forms.get("secret")
        if secret == args.deploy_secret:
            built = bottle.request.files.get("built")
            built.save(args.temp_path, overwrite=True)
            with tarfile.open(args.temp_path) as tar:
                tar.extractall(args.deploy_path)
                

    @app.route('/<:re:.*>', method=['GET', 'POST'])
    def deploy():
        xgitlab = bottle.request.headers.get('X-Gitlab-Token')
        with open(args.config_file, 'r') as fl:
            config = yaml.load(fl.read())
        if xgitlab is not None:  # Gitlab webhook
            log('gitlab request', xgitlab)
            if xgitlab not in config:
                raise bottle.HTTPError(404, body='No Project Provided')
            if not config[xgitlab].get('gitlab', False):
                raise bottle.HTTPError(404, body='Not a gitlab project')
            branch = config[xgitlab].get('branch')
            if bottle.request.json.get('ref').split('/')[-1] != branch:
                raise bottle.HTTPError(404, body='Not matching branch')
            proj = xgitlab
        else:
            if bottle.request.method == 'GET':
                token = bottle.request.query.get('token')
                proj = bottle.request.query.get('project')
            if bottle.request.method == 'POST':
                token = bottle.request.forms.get("token")
                proj = bottle.request.forms.get("project")
                log(proj, token)
            if proj is None:
                raise bottle.HTTPError(404, body='No Project Provided')
            if proj not in config:
                raise bottle.HTTPError(404, body='Unknown Project')
            if token is None or config[proj]['token'].strip() != token.strip():
                raise bottle.HTTPError(403, body='Invalid Token')
        # - project provided, exists and token matches
        if not config[proj].get('active', True):
            msg = "This project's auto deploy is set to inactive at this time"
            raise bottle.HTTPError(404, body=msg)
        # - only if it is active
        env = ' '.join(key + '=' + value for key, value in config[proj].get('environment', {}).items())
        env = env.strip() + ' '
        for cmd in config[proj]['script']:
            cmd = env + 'cd ' + config[proj]['workdir'] + ' && ' + cmd
            status = call(cmd, shell=True)
            if status != 0:
                string = '< {} > had exit code {}'.format(cmd, status)
                raise bottle.HTTPError(500, string)
        return 'Deployed'

    app.run(port=args.port, host=args.interface)
