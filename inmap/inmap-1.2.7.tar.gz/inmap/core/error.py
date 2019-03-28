

class ErrorController:

    # return 1 for positive result
    # return 0 for negative result

    @staticmethod
    def failed_to_resolve(output):
        """
        if we connect well with the target | no target found
        :param output:
        :return:
        """

        if "Nmap done: 0 IP addresses (0 hosts up)" in output or "Nmap done: 1 IP address (0 hosts up)" in output:
            print("Failed to resolve the target | no target found")
            return 0

        return 1

    @staticmethod
    def all_filtered(output):
        """
        if all port are filtered, then we have nothing to extract
        :param output:
        :return:
        """

        if "are filtered" in output:
            print(' '.join(output))
            return 0

        return 1

    @staticmethod
    def all_closed(output):
        """
        if all port are closed, then we have nothing to extract
        :param output:
        :return:
        """
        for line in output:
            if ("All" in line) and ("scanned" in line) and ("ports" in line):
                print(' '.join(line))
                return 0

        return 1
