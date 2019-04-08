########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""One of the several training modules of "fpga4p".

This module provides class for training model for Naive Bayes Classifier.

Function:
    start_instance: tart __init__ of the main class.

Classes:
    TrainNBC: This class provides algorithm for NBC classification.
Note:
    Every training module must be named as 'classify_...' and consists
    function 'start_instance' which returns the main class instance.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import fpga4p
import pandas
import pandas.errors
import serial
import serial.serialutil
import os
import pickle


########################################################################################################################
# M A I N   F U N C T I O N :  #########################################################################################
########################################################################################################################


def start_instance(train_data_path, byte_word_dict, usb_device):
    """
    Returns the main class instance.
    """
    return ClassifyNBC(train_data_path, byte_word_dict, usb_device)


########################################################################################################################
# M A I N   C L A S S :  ###############################################################################################
########################################################################################################################


class ClassifyNBC:
    """
    Classification class for Naive Bayes Classifier.

    Attributes:
        self._task: Task parameters.
        self._data_frame: .csv file for classification.
        self._byte_word_dict: Dict with word's codes.
        self._serial_port: Serial port for FPGA.
    """

    # ==================================================================================================================

    def __init__(self, classification_data_path, byte_word_dict, serial_port):
        self._task = [classification_data_path, 'classify_nbc', byte_word_dict, serial_port]
        try:
            self._data_frame = pandas.read_csv(self._task[0], sep=',', header=None)
        except FileNotFoundError:
            # If can't open classification file: -------------------------------------------------------------------
            fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.__init__()',
                              why=f"""can't open classification file: "{self._task[0]}" in task: {self._task}""",
                              task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        except pandas.errors.EmptyDataError:
            # If classification file is empty: -------------------------------------------------------------------------
            fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.__init__()',
                              why=f"""classification file: "{self._task[0]}" is empty in task: {self._task}""",
                              task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        else:
            try:
                word_dict_file = open(self._task[2], 'rb')
            except FileNotFoundError:
                # If can't open byte word dict file: -------------------------------------------------------------------
                fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.__init__()',
                                  why=f"""can't open byte word dict file: "{self._task[2]}" in task: {self._task}""",
                                  task_end=True)()
                # ------------------------------------------------------------------------------------------------------
            else:
                # Request ROOT rights in the terminal: -----------------------------------------------------------------
                self._byte_word_dict = pickle.load(word_dict_file)
                fail = os.system('sudo chmod 666 %s' % self._task[3])
                # ------------------------------------------------------------------------------------------------------
                if not fail:
                    try:
                        self._serial_port = serial.Serial(self._task[3], 9600, timeout=1, stopbits=2)
                    except serial.serialutil.SerialException:
                        # If wrong serial port: ------------------------------------------------------------------------
                        fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.__init__()',
                                          why=f'wrong serial port "{self._task[3]}" in task: {self._task} ',
                                          task_end=True)()
                        # ----------------------------------------------------------------------------------------------
                    else:
                        self.start()
                else:
                    # If ROOT rights was not obtain: -------------------------------------------------------------------
                    fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.__init__()',
                                      why=f'ROOT rights for serial port "{self._task[3]}" in task: {self._task}'
                                          f' did not obtain',
                                      task_end=True)()
                    # --------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def start(self):
        """
        Start calculations with FPGA.
        """

        # Send notification to the notification handler: ---------------------------------------------------------------
        fpga4p.core.Notification(where='classify.ClassifyNBC.start()',
                                 what=f'classification task {self._task} started calculation with FPGA',
                                 for_verbose=True)()
        # --------------------------------------------------------------------------------------------------------------

        # Prepare parameters: ------------------------------------------------------------------------------------------
        byte_list = [0xFF]
        width = fpga4p.core.get_byte_width(len(self._byte_word_dict[0]))
        # --------------------------------------------------------------------------------------------------------------

        # Create file for answers: -------------------------------------------------------------------------------------
        file_name = fpga4p.core.file_name_generator(self._task[0], '.csv', '_answers')
        while True:  # Change file name if file exists
            try:
                answers_file = open(file_name.__next__(), 'x')
            except FileExistsError:
                continue
            else:
                break
        # --------------------------------------------------------------------------------------------------------------

        # Generate bytes string: ---------------------------------------------------------------------------------------
        for i in range(len(self._data_frame[0])):
            row = list(self._data_frame.iloc[i, :])
            byte_list.append(int(len(row)))
            for j in range(len(row)):
                answers_file.write(str(row[j]) + ',')  # Write words in answers file
                value = int(self._byte_word_dict[0].get(str(row[j]), 0))
                width_bytes = fpga4p.core.get_byte_width(value)
                if width != width_bytes:
                    for k in range(width - width_bytes):
                        byte_list.append(0)
                byte_list.append(value)
            byte_list.append(0xFE)
        # --------------------------------------------------------------------------------------------------------------

            # Write bytes to the serial port: --------------------------------------------------------------------------
            try:
                self._serial_port.write(byte_list)
            except serial.SerialException:
                # If can't write: --------------------------------------------------------------------------------------
                fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.start()',
                                  why=f"can't write in serial port: {self._task[3]} in task {self._task}",
                                  task_end=True)()
                return 1
                # ------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------

            # Read bytes from the serial port: -------------------------------------------------------------------------
            else:
                try:
                    response = self._serial_port.read(3)
                except serial.SerialException:
                    # If can't read: -----------------------------------------------------------------------------------
                    fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.start()',
                                      why=f"can't read from serial port: {self._task[3]} in task {self._task}",
                                      task_end=True)()
                    # --------------------------------------------------------------------------------------------------
                    return 1
                else:
                    if not response:
                        # If answer is empty: --------------------------------------------------------------------------
                        fpga4p.core.Error(where='fpga4p.classify.ClassifyNBC.start()',
                                          why=f"answer is empty in serial port: {self._task[3]} in task {self._task}",
                                          task_end=True)()
                        return 1
                        # ----------------------------------------------------------------------------------------------
                    else:
                        # Write in answers file: -----------------------------------------------------------------------
                        answer = self._byte_word_dict[1].get(response[1], 'FPGA CLASSIFICATION ERROR!')
                        answers_file.write(answer + '\n')
                        # ----------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            byte_list = [0xFF]
        # Send notification to the notification handler: ---------------------------------------------------------------
        fpga4p.core.Notification(where='classify.ClassifyNBC.start()',
                                 what=f'classification task {self._task} finished',
                                 task_end=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================


########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
