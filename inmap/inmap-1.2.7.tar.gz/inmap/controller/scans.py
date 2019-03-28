from inmap.core.controller import Controller
from inmap.core.error import ErrorController
from inmap.controller.interpret import InterpretController
from inmap.helper.regex import RegexHelper
from inmap.model.host import HostModel
from inmap.model.port import PortModel

class ScanController(Controller):

    def __init__(self):
        self.host = HostModel()
        self.port = PortModel()

        super(ScanController, self).__init__()
        Controller.list_port_info = []

    def scan_all(self, **kwargs):
        """
        Use the nmap command : sudo nmap [-Pn] [-n] -sS -sV -O host|hostname
        :param kwargs:
        :return:
        """

        if 'host' not in kwargs:
            print("Give me a host to scan (ip address)")
            return 0

        Controller.host = kwargs['host']

        if 'pn' in kwargs.keys() and kwargs['pn']:
            self.cmd_scan = "sudo nmap -Pn "
        else:
            self.cmd_scan = "sudo nmap "

        # for the udp scan
        if 'udp' in kwargs.keys() and kwargs['udp']:
            self.cmd_scan += "-sU "

        if RegexHelper.check_ip_address(kwargs['host']):
            # we have a ip address
            self.cmd_scan += " -n"
        # our nmap command is ready to execute
        self.cmd_scan += " -sS -sV -O "+kwargs['host']
        self._execute()

        InterpretController.state()

        self.__save_result(True)

    def scan_ports(self, **kwargs):
        """
        Use the nmap command : nmap [-Pn] -p ports host|hostname -T5
        :param kwargs:
        :return:
        """
        if 'host' not in kwargs:
            print("Give me a host to scan (ip address)")
            return 0

        if 'ports' not in kwargs:
            print("Give me list of ports to scan: ports='0-50' ")
            return 0

        Controller.host = kwargs['host']

        if 'pn' in kwargs.keys() and kwargs['pn']:
            self.cmd_scan = "nmap -Pn "
        else:
            self.cmd_scan = "nmap "

        # for the udp scan
        if 'udp' in kwargs.keys() and kwargs['udp']:
            self.cmd_scan = "sudo "+self.cmd_scan +"-sU "

        self.cmd_scan += "-p "+kwargs['ports']+" "+kwargs['host']
        # mode faster -T5
        self.cmd_scan += " -T5"
        self._execute()

        if not ErrorController.all_closed(Controller.list_output):
            return 0

        self.__save_result()

    def scan_version_port(self, **kwargs):
        """
        Use the nmap command : nmap [-Pn] -sV -p ports host|hostname -T5
        :param kwargs:
        :return:
        """
        if 'host' not in kwargs:
            print("Give me a host to scan (ip address)")
            return 0

        if 'ports' not in kwargs:
            print("Give me list of ports to scan: ports='0-50' ")
            return 0

        Controller.host = kwargs['host']

        if 'pn' in kwargs.keys() and kwargs['pn']:
            self.cmd_scan = "nmap -Pn "
        else:
            self.cmd_scan = "nmap "

        # for the udp scan
        if 'udp' in kwargs.keys() and kwargs['udp']:
            self.cmd_scan = "sudo "+self.cmd_scan +"-sU "


        self.cmd_scan += "-sV -p " + kwargs['ports'] + " " + kwargs['host']
        # mode faster -T5
        self.cmd_scan += " -T5"
        self._execute()

        self.__save_result()

    def scan_most_ports(self, **kwargs):
        """
        Use the nmap command : nmap [-Pn] [-sV] --top-ports number host|hostname -T5
        :param kwargs:
        :return:
        """
        if 'host' not in kwargs:
            print("Give me a host to scan (ip address)")
            return 0

        Controller.host = kwargs['host']

        if 'pn' in kwargs.keys() and kwargs['pn']:
            self.cmd_scan = "nmap -Pn "
        else:
            self.cmd_scan = "nmap "

        # for the udp scan
        if 'udp' in kwargs.keys() and kwargs['udp']:
            self.cmd_scan = "sudo "+self.cmd_scan +"-sU "


        if 'number' not in kwargs:
            kwargs['number'] = 10

        if 'version' in kwargs.keys() and kwargs['version']:
            self.cmd_scan += "-sV --top-ports "+str(kwargs['number'])
        else:
            self.cmd_scan += "--top-ports "+str(kwargs['number'])

        self.cmd_scan += " "+kwargs['host']
        self.cmd_scan += " -T5"
        self._execute()

        self.__save_result()

    def scan_ports_hosts(self, **kwargs):

        if 'ports' not in kwargs:
            print("Give me list of ports to scan: ports='0-50' ")
            return 0

        if 'pn' in kwargs.keys() and kwargs['pn']:
            self.cmd_scan = "nmap -Pn "
        else:
            self.cmd_scan = "nmap "

        # for the udp scan
        if 'udp' in kwargs.keys() and kwargs['udp']:
            self.cmd_scan = "sudo "+self.cmd_scan +"-sU "

        if 'filename' in kwargs.keys():
            self.cmd_scan += "-p "+kwargs['ports'] + " -iL " + kwargs['filename']
        elif 'hosts' not in kwargs:
            print("Give me hosts to scan : 10.10.10.0/24")
            return 0
        else:
            Controller.host = kwargs['hosts']
            self.cmd_scan += "-p "+kwargs['ports'] + " " + kwargs['hosts']

        # mode faster -T5
        self.cmd_scan += " -T5"
        self._execute()

        list_outputs = []
        i = -1
        for line in self.list_output:

            if ("Nmap" in line) and ("scan" in line) and ("report" in line):
                i += 1
                list_outputs.append([])
                list_outputs[i].append(line)
            else:
                if i == -1:
                    # initialisation
                    list_outputs.append([])
                    continue
                list_outputs[i].append(line)

        # delete a empty line
        for line in list_outputs:
            if not line:
                list_outputs.remove(line)

        # test to extract
        for line in list_outputs:
            if (not ErrorController.all_closed(line)) or (not ErrorController.all_filtered(line)):

                Controller.list_output = line
                InterpretController.ip_address()
                self.__save_host_ports(
                    ip_address=ScanController.ip_address,
                    hostname=ScanController.hostname,
                    mac_address='',
                    device_type='',
                    state='',
                    os_family='',
                    os_cpe='',
                    os_details='',
                    info_host='',
                    info_os='',
                    info_cpe='',
                    network_distance='',
                    noport=True
                )

                continue

            Controller.list_output = line
            self.__save_result()

    def __save_host_ports(self, **kwargs):
        """
        Private methode to save the host and port result
        :param kwargs:
        :return:
        """

        self.host.insert_line(
            ip_address=kwargs['ip_address'],
            hostname=kwargs['hostname'],
            mac_address=kwargs['mac_address'],
            device_type=kwargs['device_type'],
            os_family=kwargs['os_family'],
            os_cpe=kwargs['os_cpe'],
            os_details=kwargs['os_details'],
            state=kwargs['state'],
            info_host=kwargs['info_host'],
            info_os=kwargs['info_os'],
            info_cpe=kwargs['info_cpe'],
            network_distance=kwargs['network_distance']
        )

        # no port insertion, just host
        if ("noport" in kwargs.values()) and kwargs["noport"]:
            return 0

        # after that we store ports
        self.port.insert_lines(ScanController.list_port_info, kwargs['ip_address'])

    def __save_result(self, all = False):
        """
        Private method, use the saves_** methods, this method is used for one or multiple results
        :param all:
        :return:
        """
        Controller.list_output.append(['Nmap', 'scan', 'report', 'for'])

        results = Controller.list_output
        Controller.list_output = []
        doit = False
        for result in results:
            if 'Nmap' in result and 'scan' in result and 'report' in result and 'for' in result:

                if doit:
                    self.__save_all() if all else self.__save()
                    Controller.list_output = []
                else:
                    doit = True

            if doit:
                Controller.list_output.append(result)

    def __save(self):
        """
        Interpret and save the result
        if we have already a host result in db, it's updated
        :return:
        """
        InterpretController.scan_port()
        # check if kwargs['host'] is an adress
        InterpretController.ip_address()

        # after interpretation we save the result, we begin by saving or getting the host
        # get host if it exists
        row = self.host.select(ip_address=ScanController.ip_address)

        if len(row) > 0:
            self.port.insert_lines(ScanController.list_port_info, ScanController.ip_address)
        else:
            # we store firstly the host
            self.__save_host_ports(
                ip_address=ScanController.ip_address,
                hostname=ScanController.hostname,
                mac_address='',
                device_type='',
                os_family='',
                os_cpe='',
                os_details='',
                state='',
                info_host='',
                info_os='',
                info_cpe='',
                network_distance='',
            )

    def __save_all(self):
        """
        Interpret and save the result
        if we have already a host result in db, it's updated
        this method is used for scan_all method
        :return:
        """
        # interpret|extract the information from the output
        InterpretController.scan_all()
        # interpret|extract the ip address and mac address
        InterpretController.ip_address()

        # we store the interpret result database
        self.__save_host_ports(
            ip_address=ScanController.ip_address,
            hostname=ScanController.hostname,
            mac_address=ScanController.mac_address,
            device_type=ScanController.device_type,
            os_family=ScanController.os_family,
            os_cpe=ScanController.os_cpe,
            os_details=ScanController.os_details,
            state=ScanController.state,
            info_host=str(ScanController.service_info_host),
            info_os=str(ScanController.service_info_host),
            info_cpe=str(ScanController.service_info_cpe),
            network_distance=ScanController.network_distance,
        )
