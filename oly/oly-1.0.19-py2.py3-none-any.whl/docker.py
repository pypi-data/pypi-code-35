import os
import subprocess
import sys
from tabulate import tabulate

from .setup import Setup
from .utils import Clr, Utils, merge
from .config import Config
from .service import Service
import shutil

SERVICES_PREFIX = 'oly_'
NETWORK = 'olynet'
DOCKER_ERROR_MISSING_NETWORK = 'Network ' + Utils.NETWORK + ' declared as external, ' \
                                'but could not be found. Please create the network ' \
                                'manually using `docker network create ' + Utils.NETWORK + '` and try again.'


class Docker:
    def __init__(self):
        pass

    def tools_run(self, tools, **kwargs):
        if len(tools) == 0:
            tools = Config().read_config()['tools']

        for tool in tools:
            kwargs['file'] = os.path.join(Utils.TOOLS_DIR, tool, tool + '.yml')
            self._run(tool, **kwargs)

    def tools_stop(self, tools, **kwargs):
        if len(tools) == 0:
            tools = Config().read_config()['tools']

        for tool in tools:
            kwargs['file'] = os.path.join(Utils.TOOLS_DIR, tool, tool + '.yml')
            self._stop(tool, **kwargs)

    def tools_ls(self, tools, **kwargs):
        self.tools_status(tools)

    @staticmethod
    def tools_status(tools, **kwargs):
        if len(tools) == 0:
            tools = Config().read_config()['tools']
        status = {"running": [], "stopped": []}
        for tool in tools:
            command = 'docker ps --filter status=running --filter name=' \
                      + tool + " --format '{{.Names}}\t{{.Ports}}'"
            process = subprocess.check_output(command, shell=True).decode(sys.stdout.encoding).strip()
            parts = str(process).split('\t')
            if len(str(process).strip()) > 1:
                ports = ''
                if len(parts) >= 2:
                    ports = str(parts[1]).rstrip("\n'")
                msg = Clr.OK + "  %-16s %-16s %s" % (str(tool) + Clr.RESET, 'Up and running', ports)
                status['running'].append(msg)
            else:
                msg = Clr.OK + "  %-16s %s" % (str(tool) + Clr.RESET, Clr.WARNING + 'Stopped' + Clr.RESET)
                status['stopped'].append(msg)
        print('')
        Clr('Tools: ').warn()
        if len(status['running']) >= 1:
            rows = "\n".join(status['running'])
            print(rows)
        if len(status['stopped']) >= 1:
            rows = "\n".join(status['stopped'])
            print(rows)

    @staticmethod
    def tools_update(tools, **kwargs):
        if len(tools) == 0:
            tools = Config().read_config()['tools']

        for tool in tools:
            tool_file = os.path.join(Utils.TOOLS_DIR, tool, tool + '.yml')
            command = 'docker ps --filter status=running --filter name=' \
                      + tool + ' --format \'{{.ID}}\\t{{.Names}}\''
            process = subprocess.check_output(command, shell=True).decode(sys.stdout.encoding).strip()

            sys.stdout.write('Updating ' + tool + ' ... ')
            if tool in process:
                command = 'docker-compose -f ' + tool_file + ' up -d --build --force-recreate'
            else:
                command = 'docker-compose -f ' + tool_file + ' build --force-rm --no-cache'

            try:
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                print(Clr.OK + 'OK' + Clr.RESET)
            except subprocess.CalledProcessError as e:
                print(Clr.FAIL + 'KO' + Clr.RESET)
                print('Cannot update ' + tool + ' Error: ' + e.output)

    @staticmethod
    def service_add(mtype, services, **kwargs):
        service = None
        if services:
            service = services[0]

        getattr(Setup(), mtype)(m_service=service)

    def service_run(self, mtype, services, **kwargs):
        p_list = []
        if mtype == 'package':
            p_list = Setup().package_list()
        elif mtype == 'service':
            p_list = Setup().all_services_list(plain=True)

        if not services and ('--all' not in list(kwargs.keys()) and '-a' not in list(kwargs.keys())):
            services = Utils().input_with_help(
                'Select one or more ' + mtype + 's to run or type '
                + Clr.OK + 'all' + Clr.RESET + ' to run them all.',
                str(mtype).capitalize() + 's: ',
                *p_list
            ).strip().split(' ')

            if 'all' in services:
                self._run_all(mtype, **kwargs)
                exit(0)

            m = []
            if services:
                for service in services:
                    service = Utils.resolve_service_from_input(mtype, service, p_list)
                    if service not in m:
                        if service:
                            getattr(self, '_run_' + mtype)(service, **kwargs)
                    else:
                        # skip more same entries
                        continue
                    m.append(service)
                exit(0)
            else:
                exit(0)

        elif '--all' in list(kwargs.keys()) or '-a' in list(kwargs.keys()):
            self._run_all(mtype, **kwargs)
            exit(0)
        elif services:
            for service in services:
                getattr(self, '_run_' + mtype)(service, **kwargs)
            exit(0)
        exit(0)

    def service_stop(self, mtype, services, **kwargs):
        p_list = []
        if mtype == 'package':
            p_list = Setup().package_list()
        elif mtype == 'service':
            p_list = Setup().all_services_list(plain=True)

        if not services and ('--all' not in list(kwargs.keys()) and '-a' not in list(kwargs.keys())):
            services = Utils().input_with_help(
                'Select one or more ' + mtype + 's to stop or type '
                + Clr.OK + 'all' + Clr.RESET + ' to stop them all.',
                str(mtype).capitalize() + 's: ',
                *p_list
            ).strip().split(' ')

            if 'all' in services:
                self._stop_all(mtype, **kwargs)
                exit(0)

            m = []
            if services:
                for service in services:
                    service = Utils.resolve_service_from_input(mtype, service, p_list)
                    if service not in m:
                        if service:
                            getattr(self, '_stop_' + mtype)(service, **kwargs)
                    else:
                        # skip more same entries
                        continue
                    m.append(service)
                exit(0)
            else:
                exit(0)

        elif '--all' in list(kwargs.keys()) or '-a' in list(kwargs.keys()):
            self._stop_all(mtype, **kwargs)
            exit(0)
        elif services:
            for service in services:
                getattr(self, '_stop_' + mtype)(service, **kwargs)
            exit(0)
        exit(0)

    def service_update(self, mtype, services, **kwargs):
        p_list = []
        if mtype == 'package':
            p_list = Setup().package_list()
        elif mtype == 'service':
            p_list = Setup().all_services_list(plain=True)

        if not services and ('--all' not in list(kwargs.keys()) and '-a' not in list(kwargs.keys())):
            services = Utils().input_with_help(
                'Select one or more ' + mtype + 's to update or type '
                + Clr.OK + 'all' + Clr.RESET + ' to update them all.',
                str(mtype).capitalize() + 's: ',
                *p_list
            ).strip().split(' ')

            if 'all' in services:
                self._run_all(mtype, **kwargs)
                exit(0)

            m = []
            if services:
                for service in services:
                    service = Utils.resolve_service_from_input(mtype, service, p_list)
                    if service not in m:
                        if service:
                            getattr(self, '_update_' + mtype)(service, **kwargs)
                    else:
                        # skip more same entries
                        continue
                    m.append(service)
                exit(0)
            else:
                exit(0)

        elif '--all' in list(kwargs.keys()) or '-a' in list(kwargs.keys()):
            self._run_all(mtype, **kwargs)
            exit(0)
        elif services:
            for service in services:
                getattr(self, '_update_' + mtype)(service, **kwargs)
            exit(0)
        exit(0)

    @staticmethod
    def service_status(mtype, services):
        plain_services = Setup().all_services_list(plain=True)
        table_services = Setup().all_services_list(table=True)
        print

        if not plain_services:
            print('No ' + mtype + 's found. Run ' + Clr.WARNING + '"oly ' + mtype + ' add"' +
                  Clr.RESET + ' to add ' + mtype + 's!')
            exit(0)

        command = 'docker ps -f status=running -f name=' \
                  + ' -f name='.join(plain_services) + ' --format \'{{.Names}}\\t{{.Ports}}\''

        process = subprocess.check_output(command, shell=True).decode(sys.stdout.encoding).strip()
        if process:
            parts = str(process).split("\n")
            if parts:
                for row in parts:
                    service, ports = row.strip().split('\t')
                    if service in table_services['Name']:
                        index = table_services['Name'].index(service)
                        table_services['Status'].pop(index)
                        table_services['Status'].insert(index, Clr.OK + 'Up' + Clr.RESET)
                        table_services['Ports'].pop(index)
                        table_services['Ports'].insert(index, ports)

        print(tabulate(table_services, headers='keys', tablefmt='simple'))

        print

    def service_remove(self, mtype, services, **kwargs):
        """
            Before removal actions:
                1 - Check if there are changes to commit with git
                2 - Check if it is running
                3 - Remove the directory, container, image and volume
        """
        p_list = []
        if mtype == 'package':
            p_list = Setup().package_list()
        elif mtype == 'service':
            p_list = Setup().all_services_list(plain=True)

        if not services and ('--all' not in list(kwargs.keys()) and '-a' not in list(kwargs.keys())):
            services = Utils().input_with_help(
                'Select one or more ' + mtype + 's to remove or type '
                + Clr.OK + 'all' + Clr.RESET + ' to remove them all.',
                str(mtype).capitalize() + 's: ',
                *p_list
            ).strip().split(' ')

            if 'all' in services:
                self._remove_all(mtype, **kwargs)
                exit(0)

            m = []
            if services:
                for service in services:
                    service = Utils.resolve_service_from_input(mtype, service, p_list)
                    if service not in m:
                        if service:
                            getattr(self, '_remove_' + mtype)(service, **kwargs)
                    else:
                        # skip more same entries
                        continue
                    m.append(service)
                exit(0)
            else:
                exit(0)

        elif '--all' in list(kwargs.keys()) or '-a' in list(kwargs.keys()):
            self._remove_all(mtype, **kwargs)
            exit(0)
        elif services:
            print(Clr.WARNING + 'Removing ' + ', '.join(services) + Clr.RESET)
            prompt = input('Continue: [y/N] ')
            if str(prompt).lower() not in ['y', 'yes']:
                exit(0)
            for service in services:
                getattr(self, '_remove_' + mtype)(service, **kwargs)
            exit(0)
        exit(0)

    def service_ls(self, mtype, services):
        self.service_status(mtype, services)

    @staticmethod
    def remove_tools():
        tools = Config().read_config()['tools']
        for tool in tools:
            print('Removing ' + tool)
            try:
                subprocess.check_call(
                    'docker system prune --filter "name=' + tool + '" --volumes -f', shell=True, stdout=subprocess.PIPE)
                return True
            except subprocess.CalledProcessError:
                return False

    @staticmethod
    def remove_all():
        """Remove all images and volumes from the system"""
        try:
            print('Removing all...')
            subprocess.check_call('docker system prune -a --volumes -f', shell=True, stdout=subprocess.PIPE)
            print('Removing all images...')
            subprocess.check_call('docker image prune -a -f', shell=True, stdout=subprocess.PIPE)
            print('Removing volumes...')
            subprocess.check_call('docker volume prune -f', shell=True, stdout=subprocess.PIPE)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def validate_services(mtype, services, action):
        s = Setup()
        sp_list = getattr(s, mtype + '_list')()

        def mhelp():
            print()
            print(Clr.WARNING + 'Usage:' + Clr.RESET)
            print('  oly ' + mtype + ' ' + action + ' [OPTION] [' + str(mtype).upper() + 'S]')
            print()
            print(Clr.WARNING + 'Available options:' + Clr.RESET)
            print(Clr.OK + '  -a, --all       ' + Clr.RESET + action.capitalize() + ' all ' + mtype + 's')
            print(Clr.OK + '  -f, --force     ' + Clr.RESET + 'Force ' + action + ' all ' + mtype + 's')
            print()
            print(Clr.WARNING + 'Available ' + mtype + 's:' + Clr.RESET)
            for i, s in enumerate(sp_list, 1):
                print('  ' + str(i) + ' - ' + Clr.OK + s + Clr.RESET)
            print()

        # if mtype == 'service':
        if not sp_list:
            print('No ' + mtype + ' found. Run ' + Clr.WARNING + '"oly ' + mtype + ' add"' + Clr.RESET + ' to add ' + mtype + 's!')
            exit(0)
        elif not services:
            print('No ' + mtype + ' selected. Select one of the following ' + mtype + 's to ' + action + '.')
            print()
            print(Clr.WARNING + 'Available ' + mtype + 's:' + Clr.RESET)
            for i, s in enumerate(sp_list, 1):
                print('  ' + str(i) + ' - ' + Clr.OK + s + Clr.RESET)
            print()
            print('Use option ' + Clr.OK + '-a|--all' + Clr.RESET + ' to ' + action + ' them all.')
            print()
            exit(0)
        elif '-h' in services or '--help' in services:
            mhelp()
            exit(0)
        elif '--all' in services or '-a' in services:
            confirm = Utils().input_with_help('Available ' + mtype + 's: ', 'Continue: [y/N]', *sp_list)
            if confirm == 'y':
                return sp_list
            exit(0)
        elif '-f' in services or '--force' in services:
            return services
        elif services:
            for s in services:
                if s not in sp_list:
                    Clr(str(mtype).capitalize() + ' ' + s + ' does not exist!').warn()
                    services.remove(s)
                    if not services:
                        print()
                        print(Clr.WARNING + 'Available ' + mtype + 's:' + Clr.RESET)
                        for i, s in enumerate(sp_list, 1):
                            print('  ' + str(i) + ' - ' + Clr.OK + s + Clr.RESET)
                        print()
                        print('Use option ' + Clr.OK + '-a|--all' + Clr.RESET + ' to ' + action + ' them all.')
                        print()
                        exit(0)

        return services

    def down(self):
        self.tools_stop([], force_recreate=True)
        self._stop_all('service')
        # remove network
        # remove_net_process = subprocess.check_output('docker network rm ' + NETWORK, shell=True)
        # print remove_net_process

    @staticmethod
    def create_network():
        command = 'docker network create ' + Utils.NETWORK
        try:
            subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as err:
            output = err.output.decode(sys.stdout.encoding).strip()
            return output

    def _run(self, service, **kwargs):
        command = 'docker-compose -f ' + kwargs['file'] + ' up -d'
        msg = 'Running ' + service + ' ... '
        if '--force-recreate' in kwargs or ('force_recreate' in kwargs and kwargs['force_recreate']):
            command += ' --build'
            msg = 'Force recreating ' + service + ' ... '
        sys.stdout.write(msg)
        try:
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            print(Clr.OK + 'OK' + Clr.RESET)
        except subprocess.CalledProcessError as err:
            if err.output.decode(sys.stdout.encoding).strip() == DOCKER_ERROR_MISSING_NETWORK:
                self.create_network()

            # retry the process
            try:
                subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                print(Clr.OK + 'OK' + Clr.RESET)
            except subprocess.CalledProcessError as err:
                error_msg = err.output.decode(sys.stdout.encoding).strip()
                if 'FileNotFoundError' in error_msg:
                    error_msg = 'docker-composer.yml file is missing '
                print(Clr.FAIL + 'KO ' + Clr.RESET + 'Cannot run ' + str(service) + ', ' + error_msg)
                print('')

    def _stop(self, service, **kwargs):
        if not self._is_service_running(service):
            return
        command = 'docker-compose -f ' + kwargs['file'] + ' down'
        if '--force-recreate' in kwargs or ('force_recreate' in kwargs and kwargs['force_recreate']):
            command += ' --rmi local --remove-orphans -v'
        sys.stdout.write('Stopping ' + service + ' ... ')
        try:
            subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)

            if self._is_service_running(service):
                # force kill the process
                subprocess.check_output('docker kill ' + service, shell=True, stderr=subprocess.STDOUT)
                subprocess.check_output('docker rm ' + service, shell=True, stderr=subprocess.STDOUT)

            print(Clr.OK + 'OK' + Clr.RESET)
        except subprocess.CalledProcessError as err:
            error_msg = err.output.decode(sys.stdout.encoding).strip()
            print(Clr.FAIL + 'KO' + Clr.RESET)
            print('Cannot stop ' + service + ' Error: ' + error_msg)

    def _remove(self, service, **kwargs):
        if Service().git_service_has_changes(service_dir=kwargs['service_dir']):
            print('')
            Clr('WARNING: \nService ' + service + ' have unsaved changes. \nIf you remove it, all changes will be lost!!!').error_banner()
            print('')
            go = input('Remove ' + service + ': [y/N] ')
            if str(go).lower() not in ['y', 'yes']:
                exit(0)
        self._stop_service(service, force_recreate=True)
        if Service().remove_service_folder(service_dir=kwargs['service_dir']):
            print('Service ' + Clr.OK + service + Clr.RESET + ' was successfully removed')

    def _update(self, service, **kwargs):
        print(Clr.OK + 'Pulling last changes from Git for ' + service + '!' + Clr.RESET)
        Service().git_service_update(service_dir=kwargs['service_dir'])

    def _run_package(self, package, **kwargs):
        files = self._get_services_composer_files()
        if package in files and files[package]:
            for service in files[package]:
                kwargs['file'] = files[package][service]
                self._run(service, **kwargs)

    def _run_service(self, service, **kwargs):
        files = self._get_services_composer_files_plain()
        if service in files and files[service]:
            kwargs['file'] = files[service]
            self._run(service, **kwargs)

    def _run_all(self, mtype, **kwargs):
        if mtype == 'package':
            m_services = Setup().all_services_list()
            for key, service in m_services.items():
                if isinstance(service, list):
                    self._run_package(key, **kwargs)
        if mtype == 'service':
            m_services = Setup().all_services_list()
            for key, service in m_services.items():
                if isinstance(service, list):
                    self._run_package(key, **kwargs)
                elif isinstance(service, str):
                    self._run_service(service, **kwargs)

    def _stop_package(self, package, **kwargs):
        files = self._get_services_composer_files()
        if package in files and files[package]:
            for service in files[package]:
                kwargs['file'] = files[package][service]
                self._stop(service, **kwargs)

    def _stop_service(self, service, **kwargs):
        files = self._get_services_composer_files_plain()
        if service in files and files[service]:
            kwargs['file'] = files[service]
            self._stop(service, **kwargs)

    def _stop_all(self, mtype, **kwargs):
        if mtype == 'package':
            m_services = Setup().all_services_list()
            for key, service in m_services.items():
                if isinstance(service, list):
                    self._stop_package(key, **kwargs)
        if mtype == 'service':
            m_services = Setup().all_services_list()
            for key, service in m_services.items():
                if isinstance(service, list):
                    self._stop_package(key, **kwargs)
                elif isinstance(service, str):
                    self._stop_service(service, **kwargs)

    def _update_service(self, service, **kwargs):
        files = self._get_services_composer_files_plain()
        if service in files and files[service]:
            kwargs['service_dir'] = os.path.dirname(files[service])
            self._update(service, **kwargs)
            self._run(service, force_recreate=True, file=files[service])

    def _update_package(self, package, **kwargs):
        files = self._get_services_composer_files()
        if package in files and files[package]:
            for service in files[package]:
                self._update_service(service, **kwargs)

    def _update_all(self, mtype, **kwargs):
        m_services = Setup().all_services_list()
        if mtype == 'package':
            for key, service in m_services.items():
                if isinstance(service, list):
                    self._update_package(key, **kwargs)
        if mtype == 'service':
            for key, service in m_services.items():
                if isinstance(service, list):
                    self._update_package(key, **kwargs)
                elif isinstance(service, str):
                    self._update_service(service, **kwargs)

    def _remove_service(self, service, **kwargs):
        dirs = self._get_services_dirs()
        if service in dirs and dirs[service]:
            kwargs['service_dir'] = dirs[service]
            self._remove(service, **kwargs)

    def _remove_all(self, mtype, **kwargs):
        if mtype == 'service':
            dirs = self._get_services_dirs()
            for service in dirs:
                kwargs['service_dir'] = dirs[service]
                self._remove(service, **kwargs)
            # Delete the remaining empty dirs (packages dirs)
            Utils.empty_dir(Utils.PROJECTS_DIR)

    def _remove_package(self, package, **kwargs):
        dirs = self._get_services_dirs()

        for service_name, service_dir in dirs.items():
            if 'pkg_' + package in service_dir:
                kwargs['service_dir'] = dirs[service_name]
                self._remove(service_name, **kwargs)

        # Delete package empty dir
        empty = True
        package_dir = os.path.join(Utils.PROJECTS_DIR, 'pkg_' + package)
        if os.path.isdir(package_dir):
            services_in_package = os.listdir(package_dir)
            for file in services_in_package:
                if os.path.isdir(file):
                    print('Service ' + file + ' cannot be removed. Remove it manually!')
                    empty = False
            if empty:
                shutil.rmtree(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + package))
        else:
            print('Package ' + Clr.WARNING + package + Clr.RESET + ' does not exist!')

    @staticmethod
    def _get_services_composer_files(filter_missing=False):
        m_services = Setup().all_services_list()
        files = {}
        missing_composer_files = {}

        for key, service in m_services.items():
            if isinstance(service, list):
                package = {key: {}}
                for s in service:
                    service_dir = os.path.join(Utils.PROJECTS_DIR, 'pkg_' + key, s)
                    if not os.path.isdir(service_dir):
                        continue
                    if os.path.isfile(os.path.join(service_dir, 'docker-compose.yml')):
                        package[key].update({s: os.path.join(service_dir, 'docker-compose.yml')})
                    else:
                        missing_composer_files.update({s: os.path.join(service_dir, 'docker-compose.yml')})
                        continue
                if package[key]:
                    files.update(package)
            elif isinstance(service, str):
                service_dir = os.path.join(Utils.PROJECTS_DIR, key)
                if not os.path.isdir(service_dir):
                    continue
                if os.path.isfile(os.path.join(service_dir, 'docker-compose.yml')):
                    files[key] = os.path.join(service_dir, 'docker-compose.yml')
                else:
                    missing_composer_files.update({service: os.path.join(service_dir, 'docker-compose.yml')})
                    continue
        if not filter_missing:
            return merge(missing_composer_files, files)

        return files

    def _get_services_composer_files_plain(self, filter_missing=False):
        m_services = self._get_services_composer_files(filter_missing)
        plain = {}
        for key, service in m_services.items():
            if isinstance(service, dict):
                for s_name, path in service.items():
                    if not filter_missing:
                        plain[s_name] = path
            elif isinstance(service, str):
                plain[key] = service

        return plain

    def _get_services_dirs(self):
        m_services = self._get_services_composer_files()
        plain = {}
        for key, service in m_services.items():
            if isinstance(service, dict):
                for s_name, path in service.items():
                        plain[s_name] = os.path.dirname(path)
            elif isinstance(service, str):
                plain[key] = os.path.dirname(service)

        return plain

    @staticmethod
    def _is_service_running(service):
        command = 'docker ps -a -f name=' + service + ' --format \'{{.ID}}\t{{.Names}}\''
        try:
            process = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode(sys.stdout.encoding).strip()
            if service in process:
                return True
        except subprocess.CalledProcessError as err:
            error_msg = err.output.decode(sys.stdout.encoding).strip()
            print(error_msg)
            exit(err.returncode)
        return False




































