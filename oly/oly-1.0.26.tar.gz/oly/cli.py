import sys
import getopt
import click

from .docker import Docker
from .help import Help
from .utils import Clr, Utils
from .config import Config

def oly(argv):
    try:
        o = Docker()
        opts, args = getopt.getopt(argv, "hva", ["help", "version"])

        # first level args
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                Help().get_help()
                sys.exit(0)
            elif opt in ("-v", "--version"):
                current_ver = Utils.VERSION
                print(current_ver)

                new_ver = Utils.check_version(current_ver)
                if new_ver:
                    print('')
                    print('New version of oly (' + Clr.OK + current_ver + ' => ' + new_ver + Clr.RESET + ') is available. Run "pip install oly --upgrade" to update.')
                    print('')
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
            Config().configure()
            exit(0)

        # check config
        if not Config.config_exists():
            print('')
            Clr('Oly is not configured, run "oly config" to setup.').error_banner()
            print('')
            exit(0)

        # console
        if args[0] == 'console':
            opts, service = getopt.getopt(args[1:], "hr", ["help", "remote"])
            remote = False
            for opt, arg in opts:
                if opt in ['-h', '--help']:
                    print(Clr.WARNING + 'Usage:' + Clr.RESET)
                    print('  oly console [OPTIONS] [SERVICE]')
                    print('')
                    print(Clr.WARNING + 'Options:' + Clr.RESET)
                    print(Clr.OK + '  -r, --remote' + Clr.RESET + '\t\tConnect to a remote container (requires rancher-cli)')
                    print('')
                    exit(0)
                elif opt in ['-r', '--remote']:
                    remote = True

            Docker.console(service, remote=remote)
            exit(0)

        # log
        if args[0] == 'log':
            opts, service = getopt.getopt(args[1:], "hr", ["help", "remote"])
            remote = False
            for opt, arg in opts:
                if opt in ['-h', '--help']:
                    print(Clr.WARNING + 'Usage:' + Clr.RESET)
                    print('  oly log [OPTIONS] [SERVICE]')
                    print('')
                    print(Clr.WARNING + 'Options:' + Clr.RESET)
                    print(Clr.OK + '  -r, --remote' + Clr.RESET + '\t\tConnect to a remote container (requires rancher-cli)')
                    print('')
                    exit(0)
                elif opt in ['-r', '--remote']:
                    remote = True

            Docker.log(service, remote=remote)
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

            Config.dump(no_security)
            click.echo()
            exit(0)

        # TOOLS
        if args[0] == 'tools':
            if len(args) > 1 and args[1] in Help.ARGUMENTS:
                tools_args = sys.argv[3:]
                force_recreate = False
                opts1, args1 = getopt.getopt(tools_args, 'ha', ['help', 'all', 'force-recreate'])
                tools = Config().read_config()['tools']
                if args[1] in ('run', 'stop'):
                    if '--force-recreate' in tools_args:
                        force_recreate = True
                        tools_args.remove('--force-recreate')
                    if len(args) == 2 and not opts1:
                        confirm = Utils.m_input(
                            str(args[1]).capitalize() + ' ' + Clr.OK + ', '.join(
                                tools) + Clr.RESET + ': [n/Y]'
                        )
                        if confirm in ['y', '']:
                            getattr(o, 'tools_' + args[1])([], force_recreate=force_recreate)
                        exit(0)
                    if len(args) > 2 and not opts1:
                        for tool_name in tools_args:
                            if tool_name not in Config().read_config()['tools']:
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
                    if tool_name not in tools:
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