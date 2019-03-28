import subprocess
from inmap.core.error import ErrorController


class Controller:
    """
    This class is the base class for all controller classes
    """

    # return 1 for positive result
    # return 0 for negative result

    # protected method
    def _execute(self):
        """
        Execute the command line and put the result in self.output
        :return:
        """
        p = subprocess.Popen(self.cmd_scan, shell=True, stdout=subprocess.PIPE)
        self.output, Controller.error = p.communicate()
        self.output = self.output.decode('utf-8')
        # splite the output string in list
        self.__str_to_list()

        ErrorController.failed_to_resolve(self.output)

    # private method
    def __str_to_list(self):
        """
        split the output string in list of list: lines of words
        """
        # check if all ports are filtered
        if not ErrorController.all_filtered(self.output):
            return 0

        list_output = self.output.split('\n')

        # split the line  on line of words
        for i in range(len(list_output)):
            list_output[i] = list_output[i].split(' ')

        # assertion and remove the empties words
        Controller.list_output = []
        for i in range(len(list_output)):
            Controller.list_output.append([])
            # len of each line(element of the list)
            x = range(len(list_output[i]))
            for j in x:
                if list_output[i][j] and len(list_output[i][j]) != 0:
                    Controller.list_output[i].append(list_output[i][j])

        # remove the emtpy line
        size = len(Controller.list_output)
        i = 0
        while i < size:
            if len(Controller.list_output[i]) == 0:
                Controller.list_output.pop(i)
                size -= 1
            i += 1

