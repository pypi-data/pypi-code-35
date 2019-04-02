import os
from collections import OrderedDict

from .config import Config
from .utils import Utils, Clr
from .bitbucket import BitBucketApi


class Setup:
    def __init__(self):
        pass

    @staticmethod
    def service(package_dir=None, m_service=None):
        i = 0
        pkg_txt = ' '
        pkg_input_hint = ''

        if package_dir:
            pkg_path = os.path.normpath(package_dir)
            pkg_split_path = pkg_path.split(os.sep)
            pkg_name = pkg_split_path.pop()
            pkg_name = pkg_name.split("pkg_")[1]
            pkg_txt = " to " + Clr.WARNING + str(pkg_name) + Clr.RESET + Clr.OK + " package "
            pkg_input_hint = Clr.WARNING + "[package " + pkg_name + "]" + Clr.RESET

        while True:

            if i == 0:
                print("\n" + Clr.OK + "Add a service" +
                      pkg_txt + "or leave empty to skip." + Clr.RESET +
                      "(Git repository name/slug recommended)")
            elif i >= 1:
                print("\n" + Clr.OK + "Add another service" + pkg_txt + Clr.RESET + "(leave empty to skip)")

            if not m_service:
                service = Utils.m_input('Service Name' + pkg_input_hint + ': ')
            else:
                service = m_service
                m_service = None

            service_dir = os.path.join(Utils.PROJECTS_DIR, service)

            if package_dir:
                service_dir = os.path.join(package_dir, service)

            if service:

                if not os.path.exists(service_dir):
                    user = Config().get_bit_bucket_username()
                    password = Config().get_bit_bucket_pass()
                    print('Fetch service from bit-bucket...')
                    repo = BitBucketApi(user, password).get_repos(query_filter='name ~ "' + service + '"')

                    if not repo['values']:
                        Clr('Repository "' + service + '" does not exist on BitBucket. Add it manually!!!').warn()
                        i += 1
                        continue

                    elif len(repo['values']) == 1:
                        repo = repo['values'][0]

                        print('This repo is found in BitBucket "' + Clr.OK + repo['name'] + Clr.RESET +
                              ' (' + repo['links']['html']['href'] + ')".')
                        confirmation = Utils.m_input('Continue: [n/Y]')

                        if confirmation in ['y', '']:
                            BitBucketApi(user, password).clone_service(repo, package_dir)

                    elif len(repo['values']) >= 2:
                        c = 0
                        print("\nMore then one repo is found on BitBucket:")
                        repos = {}
                        for r in repo['values']:
                            repos[r['slug']] = r
                            c += 1
                            print("  [" + str(c) + "] " + Clr.OK + r['slug'] + Clr.RESET)

                        print("Type " + Clr.WARNING + "'all'" + Clr.RESET + " "
                              "to add them all or enter names separated by space.")
                        print('')
                        service = Utils.m_input('Service Name' + pkg_input_hint + ': ')
                        if service:
                            if service == 'all':
                                for slug, s in repos.items():
                                    BitBucketApi(user, password).clone_service(s, package_dir)
                            else:
                                services = service.split(' ')
                                for s in services:
                                    if s in repos:
                                        BitBucketApi(user, password).clone_service(repos[s], package_dir)
                                    else:
                                        print("Service " + Clr.WARNING + service + Clr.RESET + " does not exist!")
                                        i += 1
                                        continue
                        else:
                            i += 1
                else:
                    print('Service "' + service + '" already exists. Run ' +
                          Clr.WARNING + '"oly service ls"' + Clr.RESET +
                          ' to list all available services')
                i += 1
            else:
                break

    def package(self, m_service=None):
        i = 0
        while True:
            if not m_service:
                if i == 0:
                    print("\n" + Clr.OK + "Add new or an existing package name" + Clr.RESET + " (leave empty to skip)")
                elif i >= 1:
                    print("\n" + Clr.OK + "Add another package" + Clr.RESET + " (leave empty to skip)")

                packages = self.package_list()

                if packages:
                    package = Utils().input_with_help('Existing packages: ', 'Package Name: ', *packages)
                else:
                    package = input('Package Name: ')

                if package:
                    if not os.path.exists(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + package)):
                        os.makedirs(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + package))
                    else:
                        print('')
                        print('Package "' + package + '" already exists. Run ' +
                              Clr.WARNING + '"oly package ls"' + Clr.RESET +
                              ' to list all available packages')

                    self.service(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + package))
                    i += 1
                else:
                    break
            else:
                if not os.path.exists(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + m_service)):
                    os.makedirs(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + m_service))
                else:
                    print('')
                    print('Package "' + m_service + '" already exists. Run ' +
                          Clr.WARNING + '"oly package ls"' + Clr.RESET +
                          ' to list all available packages')
                self.service(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + m_service))
                m_service=None
                i += 1

    @staticmethod
    def package_list():
        packages = os.listdir(os.path.join(Utils.PROJECTS_DIR))
        pkgs_dict = {}
        names = []
        for pkg in packages:
            if os.path.isdir(os.path.join(Utils.PROJECTS_DIR, pkg)) and 'pkg_' in pkg:
                name = pkg.split('pkg_')[1]

                names.append(name)
        return names

    @staticmethod
    def service_list():
        packages = os.listdir(os.path.join(Utils.PROJECTS_DIR))
        names = []
        for pkg in packages:
            if os.path.isdir(os.path.join(Utils.PROJECTS_DIR, pkg)) and 'pkg_' not in pkg:
                names.append(pkg)
        return names

    def all_services_list(self, **kwargs):
        services = self.service_list()
        packages = self.package_list()
        services_list = {}
        table = OrderedDict([('Name', []), ('Package', []), ('Status', []), ('Ports', [])])

        if services:
            for srv_name in services:
                services_list[srv_name] = srv_name
                if 'table' in kwargs and kwargs['table']:
                    table['Name'].append(srv_name)
                    table['Package'].extend('-')
                    table['Status'].append(Clr.WARNING + 'Stopped' + Clr.RESET)
                    table['Ports'].append('-')
        if packages:
            for pkg_name in packages:
                cdirs = os.listdir(os.path.join(Utils.PROJECTS_DIR, 'pkg_' + str(pkg_name)))
                for service in cdirs:
                    service_dir = os.path.join(Utils.PROJECTS_DIR, 'pkg_' + str(pkg_name), service)
                    if not os.path.isdir(service_dir):
                        cdirs.remove(service)

                if 'plain' in kwargs and kwargs['plain']:
                    for srv_name in cdirs:
                        services_list[srv_name] = srv_name
                elif 'table' in kwargs and kwargs['table']:
                    for srv_name in cdirs:
                        table['Name'].append(srv_name)
                        table['Package'].append(pkg_name)
                        table['Status'].append(Clr.WARNING + 'Stopped' + Clr.RESET)
                        table['Ports'].append('-')
                    services_list = table
                else:
                    services_list[pkg_name] = cdirs

        return services_list
