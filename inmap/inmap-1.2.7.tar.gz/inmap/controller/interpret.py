from inmap.core.controller import Controller
from inmap.helper.helpers import Helpers
from inmap.helper.regex import RegexHelper


class InterpretController(Controller):
    """
        These methods are used to interpret the results of the *** scan methods of the class ScanController
    """

    @staticmethod
    def scan_all():
        """
        if the scan_all is correctly executed, the output is:
        after the line : PORT     STATE     SERVICE     VERSION
                         [0]        [1]       [2]         [3] [4] ....

                        MAC |Address: |08:00:27:16:81:0B |(Oracle |VirtualBox |virtual |NIC) |
                        [0]     [1]     [2]                 [3]         [4]     [5]     [6]

                        .....
        :return:
        """

        # interpret|extract the ports
        InterpretController.extract_port()
        # interpret|extract the mac address
        InterpretController.mac_address()
        # interpret|extract the device type
        InterpretController.device_type()
        # interpret|extract the os_family system
        InterpretController.os_family()
        # interpret|extract the OS CPE
        InterpretController.os_cpe()
        # interpret|extract the OS details
        InterpretController.os_details()
        # interpret|extract the state
        InterpretController.state()
        # interpret|extract the network distance
        InterpretController.network_distance()

        dicts = InterpretController.extract_v2("Hosts:")

        if dicts:
            Controller.service_info_host = dicts['Hosts:'] if 'Hosts:' in dicts else ''
            Controller.service_info_os = dicts['OSs:'] if 'OSs:' in dicts else ''
            Controller.service_info_cpe = dicts['CPE:'] if 'CPE:' in dicts else ''
        else:
            # try another way
            Controller.service_info_host = ''
            Controller.service_info_os = ''
            Controller.service_info_cpe = ''

            InterpretController.service_info()


    @staticmethod
    def scan_port():

        # interpret|extract the ports
        InterpretController.extract_port()

    @staticmethod
    def scan_version_port():

        # interpret|extract the ports
        InterpretController.extract_port()

        dicts = InterpretController.extract_v2("Hosts:")

        Controller.service_info_host = dicts['Hosts:'] if 'Hosts:' in dicts else ''
        Controller.service_info_os = dicts['OSs:'] if 'OSs:' in dicts else ''
        Controller.service_info_cpe = dicts['CPE:'] if 'CPE:' in dicts else ''

    @staticmethod
    def network_distance():
        """
        Network |Distance: |1 |hop |
        :return:
        """
        Controller.network_distance = InterpretController.extract("Network", "Distance:")

    @staticmethod
    def ip_address():
        """
         Extract the ip address and mac address from host or search the other
        """
        output = InterpretController.extract("Nmap", "scan", "report", "for")
        output = output.split(' ')

        if len(output) >= 3:
            Controller.hostname = output[1]
            Controller.ip_address = RegexHelper.get_ip_address(output[2])
        elif len(output) == 2:
            Controller.hostname = output[0]
            Controller.ip_address = RegexHelper.get_ip_address(output[1])
        else:
            print("Failed to resolve ", Controller.host)
            return 0

    @staticmethod
    def service_info():
        """
        It's a little bit different : one line contain more information to extract
        Service Info: Host:  ack.nmap.org
        We can notice that every single information is delimited by :information|information;
        :return:
        """
        os_host = InterpretController.extract("Service Info:", "Host:")
        Controller.service_info_host = os_host



    @staticmethod
    def mac_address():
        """
        MAC |Address: |08:00:27:16:81:0B |(Oracle |VirtualBox |virtual |NIC) |
        [0]     [1]     [2]                 [3] ....
        :param mac_addres: line (list[i])
        :return:
        """
        Controller.mac_address = InterpretController.extract("MAC", "Address:")
        Controller.mac_address = RegexHelper.get_mac_address(Controller.mac_address)

    @staticmethod
    def device_type():
        """
        Interpret and extract the device type,
            Device |type: |general |purpose |
            [0]      [1]    [2]      [3]

        then the type begin of the 2 index ...

        :return:
        """
        Controller.device_type = InterpretController.extract("Device", "type:")

    @staticmethod
    def os_family():
        """
        ['os_family:', 'Linux', '3.6.X']

        :return:
        """
        Controller.os_family = InterpretController.extract("Running:")

    @staticmethod
    def os_cpe():
        """
        OS |CPE: |cpe:/o:linux:linux_kernel:2.6 |

        :return:
        """
        Controller.os_cpe = InterpretController.extract("OS", "CPE:")

    @staticmethod
    def os_details():
        """
        OS |details: |Linux |2.6.9 |- |2.6.33 |

        :return:
        """
        os_detials = InterpretController.extract("OS", "details:")

        if not os_detials:
            os_detials = InterpretController.extract("Aggressive", "OS", "guesses:")

        Controller.os_details = os_detials

    @staticmethod
    def state():
        """
        Host is up
        Note: Host seems down

        :return:
        """

        # if we have the Host is up in output ==> up
        # elsif we have Note: Host seems down ==> down

        for output in Controller.list_output:

            if 'Host' in output and 'is' in output and 'up' in output:
                state = 'Up'
                break
            elif 'Note:' in output and 'Host' in output and 'seems' in output and 'down.' in output:
                state = 'Down'
                break
            else:
                state = 'unknown'

        Controller.state = state

    @staticmethod
    def extract(*args):
        """
        this method is used for extract information from the result
        :param args: list of word to search for extract information
        :return: the extract information

        we search the correct line, we store it's index
        j : the begin index to the end of line(because we want all the rest of line)
        nbr of arguments it's the start index
        """

        i = 0
        check = False
        while i < len(Controller.list_output):
            check = True
            for word in args:
                if word not in Controller.list_output[i]:
                    check = False

            # check = True if all word in args exists in Controller.list_output[i], and i is the current line
            if check:
                break

            i += 1

        if not check:
            return ""

        str_search = ""
        j = len(args)
        while j < len(Controller.list_output[i]):
            str_search += " " + Controller.list_output[i][j]
            j += 1

        Controller.list_output.pop(i)

        return str_search

    @staticmethod
    def extract_v2(arg):
        """
        this method is used for extract information from the result
        it's for the line like
        Service |Info: |Hosts: |metasploitable.localdomain, |localhost, |irc.Metasploitable.LAN; |OSs: |Unix, |Linux; |CPE: |cpe:/o:linux:linux_kernel |
        We can notice that every single information is delimited by :information|information;

        We begin by searching Host: and begin extract information until the ;
        and see the next word that had : and so on

        :param args: list of word to search for extract information: Just Host:
        :return: the extract information
        """
        dicts = {}
        i = 0
        while i < len(Controller.list_output):
            # we search the right line
            if arg in Controller.list_output[i]:
                Controller.list_output[i][-1] += ";"    # Because we used in the test bellow
                index = Controller.list_output[i].index(arg) + 1
                list_w = []
                while index < len(Controller.list_output[i]):
                    # if true ==> the end of extraction for this arg
                    if ';' in Controller.list_output[i][index]:
                        word = Controller.list_output[i][index].rstrip(",")
                        word = word.rstrip(";")
                        list_w.append(word)
                        dicts[arg] = list_w
                        list_w = []
                        # the if the fin of the line
                        if index + 1 >= len(Controller.list_output[i]):
                            break
                        arg = Controller.list_output[i][index+1]
                        index += 1
                        continue
                    # else
                    word = Controller.list_output[i][index].rstrip(",")
                    word = word.rstrip(";")
                    list_w.append(word)

                    index += 1
                Controller.list_output.pop(i)
            i += 1

        return dicts

    @staticmethod
    def extract_port():
        """
        The extract the information about ports
        :return:
        """
        if len(Controller.list_output) == 0:
            return 0

        found_ports = False
        start_at = 0
        i = 0
        version_field = False
        # find the index of the right line : PORT   STATE   SERVICE
        while i < len(Controller.list_output):
            if ("PORT" in Controller.list_output[i]) and ("STATE" in Controller.list_output[i]) and (
                    "SERVICE" in Controller.list_output[i]):
                start_at = i
                found_ports = True
                version_field = True if 'VERSION' in Controller.list_output[i] else False
                # delete the title line: PORT | STATE ....
                Controller.list_output.pop(i)
            i += 1

        if not found_ports:
            return 0

        i = start_at
        j = 0

        while i < len(Controller.list_output):
            Controller.list_port_info.append({})
            portocol = Controller.list_output[i][0].split('/')
            Controller.list_port_info[j]['port'] = int(portocol[0])  # port
            Controller.list_port_info[j]['proto'] = portocol[1]  # protocol
            Controller.list_port_info[j]['state'] = Controller.list_output[i][1]  # state
            Controller.list_port_info[j]['service'] = Controller.list_output[i][2]  # service

            if version_field:
                # version is the rest of this line if we have
                version = Helpers.list_to_str(Controller.list_output[i][3:])
                Controller.list_port_info[j]['version'] = version  # version
            else:
                Controller.list_port_info[j]['version'] = ''  # version

            # remove this line ofter interpretation
            Controller.list_output.pop(i)
            # after deleting a line we don't have an incrementation
            j += 1
            # next line ( after incrementation )
            if (i >= len(Controller.list_output)) or (not RegexHelper.check_port_prot(Controller.list_output[i][0])):
                break
