import os
import subprocess
import sys
import getopt

from .docker import Docker
from .help import Help
from .utils import Clr, Utils
from .config import Config, SysConfig
from .bitbucket import BitBucketApi


def oly(argv):
    try:
        o = Docker()
        opts, args = getopt.getopt(argv, "hva", ["help", "version"])

        # first level args
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Help().get_help()
                sys.exit()
            elif opt in ("-v", "--version"):
                curr_ver = Help.VERSION
                new_ver = curr_ver
                user = SysConfig().get_bit_bucket_username()
                password = SysConfig().get_bit_bucket_pass()
                bb = BitBucketApi(user, password).get_repo_last_tag(Utils.BASE_NAME)

                if bb:
                    new_ver = bb[0]['name']

                print(curr_ver)
                print(new_ver)


                if new_ver != curr_ver:
                    print('New version is available (' + Clr.WARNING + new_ver + Clr.RESET + '). Run "' + Clr.OK + 'oly self-update' + Clr.RESET + '" to update')
                else:
                    print(Help.VERSION)
                exit(0)

        if len(args) == 0:
            Help().get_help()
            sys.exit()

        # second level args
        if args[0] not in Help.COMMANDS:
            Help().get_help()
            sys.exit()

        # config
        if len(args) == 1 and args[0] == 'config':
            SysConfig().setup()
            exit(0)

        # self update
        if args[0] == 'self-update':
            curr_ver = Help.VERSION
            new_ver = curr_ver
            user = SysConfig().get_bit_bucket_username()
            password = SysConfig().get_bit_bucket_pass()
            bb = BitBucketApi(user, password).get_repo_last_tag(Utils.BASE_NAME)

            if bb:
                new_ver = bb[0]['name']

            if new_ver == curr_ver:
                Clr('You are already using oly latest version ' + curr_ver + ' (stable channel).').ok()
                print('')
                exit(0)

            print('Updating to version ' + Clr.OK + new_ver + Clr.RESET + ' (stable channel).')
            BitBucketApi(user, password).self_update()
            f = open(os.path.join(Utils.ROOT_DIR, 'version'), 'w+')
            f.write(new_ver)
            f.close()
            print('')
            exit(0)

        # uninstall
        if args[0] == 'uninstall':
            try:
                confirm = Utils.m_input('Uninstall oly: [y/N]')
                if confirm == 'y':
                    Docker().tools_stop([], force_recreate=True)
                    # TODO:: also remove all images from docker
                    uninstall = os.path.join(Utils.ROOT_DIR, 'uninstall')
                    subprocess.check_call(uninstall, shell=True)
                exit(0)
            except subprocess.CalledProcessError:
                exit(1)

        # check config
        if not Config().get_sys_config():
            print('')
            Clr('Oly is not configured, run "oly config" to setup.').error_banner()
            print('')
            exit(0)

        # status
        if args[0] == 'status':
            Docker().tools_status([])
            Docker().service_status('service', [])
            exit(0)

        # down
        if args[0] == 'down':
            Docker().down()
            exit(0)

        # dump config
        if args[0] == 'dump-config':
            bump = sys.argv[2:]
            dcopt, dcarg = getopt.getopt(bump, "hn", ["help", "no-security"])
            no_security = False

            for opt, arg in dcopt:
                if opt in ("-h", "--help"):
                    Clr('Usage:').warn()
                    Clr('  oly dump-config [OPTIONS]').ok()
                    print('')
                    Clr('Available Options:').warn()
                    print(Clr.OK + "  %-25s %s" % ('-h, --help' + Clr.RESET, 'Display this help'))
                    print(Clr.OK + "  %-25s %s" % ('-n, --no-security' + Clr.RESET, 'Print passwords to stdout'))
                    print('')
                    sys.exit()
                elif opt in ("-n", "--no-security"):
                    no_security = True

            cnf = SysConfig().dump_config(no_security)
            if not cnf:
                print('')
                Clr('Oly is not configured, run "oly config" to setup.').error_banner()
            print('')
            exit(0)

        # TOOLS
        if args[0] == 'tools':
            if len(args) > 1 and args[1] in Help.ARGUMENTS:
                tools_args = sys.argv[3:]
                force_recreate = False
                opts1, args1 = getopt.getopt(tools_args, 'ha', ['help', 'all', 'force-recreate'])
                if args[1] in ('run', 'stop'):
                    if '--force-recreate' in tools_args:
                        force_recreate = True
                        tools_args.remove('--force-recreate')
                    if len(args) == 2 and not opts1:
                        confirm = Utils.m_input(
                            str(args[1]).capitalize() + ' ' + Clr.OK + ', '.join(
                                Config().get_available_tools()) + Clr.RESET + ': [n/Y]'
                        )
                        if confirm in ['y', '']:
                            getattr(o, 'tools_' + args[1])([], force_recreate=force_recreate)
                        exit(0)
                    if len(args) > 2 and not opts1:
                        for tool_name in tools_args:
                            if tool_name not in Config().get_available_tools():
                                Clr("Tool '" + tool_name + "' does not exist!").warn()
                                tools_args.remove(tool_name)

                        getattr(o, 'tools_' + args[1])(tools_args, force_recreate=force_recreate)
                        exit(0)
                    elif opts1[0][0] in ('-a', '--all'):
                        getattr(o, 'tools_' + args[1])([], force_recreate=force_recreate)
                        exit(0)
                    elif opts1[0][0] in ('-h', '--help'):
                        Help().tools_help(args)
                        exit(0)

                for tool_name in tools_args:
                    if tool_name not in Config().get_available_tools():
                        Clr("Tool '" + tool_name + "' does not exist!").warn()
                        tools_args.remove(tool_name)

                getattr(o, 'tools_' + args[1])(tools_args, force_recreate=force_recreate)
                exit(0)
            else:
                Help().get_args_help(args[0])

        # SERVICES & PACKAGES
        elif args[0] in ['service', 'package']:
            if len(args) > 1 and args[1] in Help().SERVICES_ARGUMENTS:
                opts, services = getopt.getopt(args[2:], 'ha', ['help', 'all', 'force-recreate'])
                opts = dict(opts)
                if '--force-recreate' in services:
                    opts['force_recreate'] = True
                    services.remove('--force-recreate')
                getattr(o, 'service_' + args[1])(args[0], services, **opts)
            else:
                Help().services_help(args[0])
            exit(0)
        else:
            Help().get_args_help(args[0])

        exit(0)
    except getopt.GetoptError:
        Help().get_help()
        exit(0)

def start():
    oly(sys.argv[1:])


if __name__ == "__main__":
    oly(sys.argv[1:])