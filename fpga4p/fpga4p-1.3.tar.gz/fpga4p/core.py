########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""
Control module of "fpga4p".

This module provides execution of the tasks in the separate processes and
synchronized output in the terminal. Also there are classes for printing
errors and notifications.

Classes:
    Core: The main class.
    Error: For printing errors.
    Notification: For printing notifications.

Decorators:
    @notification_event_generator: For synchronized output in the terminal.
    @check_if_queue_is_empty: For synchronized output in the terminal.

Functions:
    file_name_generator: Generate file name for existing file.
    get_byte_width: Count byte size for variables in FPGA.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import singleton_decorator
import multiprocessing
import threading
import datetime
import serial
import serial.tools.list_ports
import itertools
# Import characters for special output in the terminal: ----------------------------------------------------------------
from fpga4p.start import *
# ----------------------------------------------------------------------------------------------------------------------


########################################################################################################################
# D E C O R A T O R :  #################################################################################################
########################################################################################################################


def notification_event_generator(print_notification):
    """
    Decorator, which generates event for every called notification.

    Args:
        print_notification: Function for wrapping, which might generates
            notification event.
    Returns:
        function: Wrapper for function.
    """
    def wrapper(self, notification):
        # Call wrapped method: -----------------------------------------------------------------------------------------
        print_notification(self, notification)
        # --------------------------------------------------------------------------------------------------------------

        # After that, set notification event: --------------------------------------------------------------------------
        self._set_notification_event()
        # --------------------------------------------------------------------------------------------------------------
    return wrapper


########################################################################################################################
# D E C O R A T O R :  #################################################################################################
########################################################################################################################


def check_if_queue_is_empty(get_notification_from_queue):
    """
    Decorator, which turns off notification event if queue is empty.

    Args:
        get_notification_from_queue: Function for wrapping, which might check it.
    Returns:
        function: Wrapper for function.
    """
    def wrapper(self):
        # Check if notification queue is empty: ------------------------------------------------------------------------
        try:
            notification = get_notification_from_queue(self)
        # --------------------------------------------------------------------------------------------------------------

        # If it is, unset notification event and return None: ----------------------------------------------------------
        except IndexError:
            self._notification_event.clear()
            return None
        # --------------------------------------------------------------------------------------------------------------
        else:
            return notification
    return wrapper


########################################################################################################################
# M A I N   C L A S S :  ###############################################################################################
########################################################################################################################


@singleton_decorator.singleton
class Core:
    """
    The main class.

    This class provides execution of the tasks in the separate processes and
    synchronized output in the terminal.

    Attributes:
        self._kwargs: Task strings from the terminal.
        self._manager: The Manager for synchronization.
        self._queue: The queue for notifications and errors.
        self._notification_event: Event of new notification.
        self._notification_thread: The thread for notification handling.
        self._classify_task_dict: The queue of classification tasks.
        self._task_counter: Task counter for stopping notification loop.
    """

    # ==================================================================================================================

    def __init__(self):
        # Attributes bounded with tasks execution: ---------------------------------------------------------------------
        self._kwargs = None
        self._classification_task_dict = {}
        for port in serial.tools.list_ports.comports():  # Declaration of task queues for different FPGAs
            self._classification_task_dict[port.device] = []
        # --------------------------------------------------------------------------------------------------------------

        # Attributes bounded with notification handler: ----------------------------------------------------------------
        self._manager = multiprocessing.Manager()
        self._queue = self._manager.list()
        self._notification_event = self._manager.Event()
        self._notification_thread = threading.Thread(target=self._notification_handler)
        self._task_counter = multiprocessing.Value('i', 0)
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def set_kwargs(self, trn, cls, verbose):
        """
        Set task strings from the terminal.
        """

        # Check too few arguments error: -------------------------------------------------------------------------------
        if trn is None and cls is None:
            Error(where='fpga4p.core.Core.set_kwargs()',
                  why='too few arguments',
                  fatal=True,
                  task_end=True)()
        # --------------------------------------------------------------------------------------------------------------

        # Set task strings as attribute: -------------------------------------------------------------------------------
        self._kwargs = {'trn': trn, 'cls': cls, 'verbose': verbose}
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def start(self):
        """
        Start tasks executing in separate processes.
        """

        # Start notification handler in the separate thread: -----------------------------------------------------------
        self._task_counter.value += 1  # Notification handler consider as one of the tasks
        self._notification_thread.start()
        # --------------------------------------------------------------------------------------------------------------

        # Extract arguments from the training task strings: ------------------------------------------------------------
        if self._kwargs['trn']:
            for arg in self._training_arguments_extract():
                # Every training task must have exactly 2 arguments: ---------------------------------------------------
                if len(arg) != 2:
                    Error(where='fpga4p.core.Core.start()',
                          why=f'wrong number of arguments for training task: {arg}')()
                # ------------------------------------------------------------------------------------------------------
                else:
                    self._start_train(arg[0], arg[1])
        # --------------------------------------------------------------------------------------------------------------

        # Extract arguments from the classification task strings: ------------------------------------------------------
        if self._kwargs['cls']:
            for arg in self._classification_arguments_extract():
                # Every classification task must have exactly 4 arguments: ---------------------------------------------
                if len(arg) != 4:
                    Error(where='fpga4p.core.Core.start()',
                          why=f'wrong number of arguments for classification task: {arg}')()
                # ------------------------------------------------------------------------------------------------------
                else:
                    self._add_classify_queue(arg[0], arg[1], arg[2], arg[3])
        # --------------------------------------------------------------------------------------------------------------

        # Execute separate process for task queue for every FPGA: ------------------------------------------------------
        for task_queue in self._classification_task_dict.values():
            classification_process = multiprocessing.Process(target=self._start_classify_queue, args=(task_queue,))
            classification_process.daemon = True
            classification_process.start()
        # --------------------------------------------------------------------------------------------------------------

        # Send notification to the notification handler: ---------------------------------------------------------------
        Notification(where='fpga4p.core.Core.start()',
                     what='all tasks started',
                     task_end=True,
                     for_verbose=True)()
        # --------------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _training_arguments_extract(self):
        """
        Get arguments from training task string.
        """
        arg_list = self._kwargs.get('trn').split(';')
        for arg in arg_list:
            yield arg.split(',')

    # ==================================================================================================================

    def _classification_arguments_extract(self):
        """
        Get arguments from classification task string.
        """
        arg_list = self._kwargs.get('cls').split(';')
        for arg in arg_list:
            yield arg.split(',')

    # ==================================================================================================================

    # Set notification event: ------------------------------------------------------------------------------------------
    @notification_event_generator
    # ------------------------------------------------------------------------------------------------------------------
    def print_notification(self, notification):
        """
        Send notification or error instance to the notification queue.
        """
        self._queue.append(notification)

    # ==================================================================================================================

    # Check notification queue: ----------------------------------------------------------------------------------------
    @check_if_queue_is_empty
    # ------------------------------------------------------------------------------------------------------------------
    def _get_notification_from_queue(self):
        """
        Get notification or error instance from the notification queue.
        """
        return self._queue.pop(0)

    # ==================================================================================================================

    def _set_notification_event(self):
        """
        Set notification event.
        """
        self._notification_event.set()

    # ==================================================================================================================

    def _notification_handler(self):
        """
        This loop handles notifications and errors from queue.
        """
        while self._task_counter.value != 0:  # Endless loop, while not all tasks are finished
            # Waiting for new notification: ----------------------------------------------------------------------------
            self._notification_event.wait()
            # ----------------------------------------------------------------------------------------------------------

            # Print new notification: ----------------------------------------------------------------------------------
            notification = self._get_notification_from_queue()
            if notification is None:
                continue
            else:
                # Check if the notification is for verbose mode only: --------------------------------------------------
                if self._kwargs.get('verbose'):
                    notification.output()
                elif not notification.for_verbose():
                    notification.output()
                # ------------------------------------------------------------------------------------------------------

                # Subtract 1 from the task counter if the task finished: -----------------------------------------------
                if notification.task_end():
                    self._task_counter.value += -1
                # ------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------

    # ==================================================================================================================

    def _start_train(self, training_data_path, training_class):
        """
        Execute the training task.
        """
        self._task_counter.value += 1
        # Try to find passed training class: ---------------------------------------------------------------------------
        try:
            train_module = getattr(fpga4p.train, training_class)
        # --------------------------------------------------------------------------------------------------------------
        except AttributeError:
            # If passed training class is unavailable: -----------------------------------------------------------------
            Error(where='fpga4p.core.Core._start_train()',
                  why=f'wrong train class "{training_class}" in task: {[training_data_path, training_class]}',
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        else:
            train_module.start_instance(training_data_path)  # Training classes inherits multiprocessing.Process

    # ==================================================================================================================

    def _add_classify_queue(self, classification_data_path, classification_class, byte_word_dict, serial_port):
        """
        Append classification task in the queue for concrete FPGA.
        """
        self._task_counter.value += 1
        task = [classification_data_path, classification_class, byte_word_dict, serial_port]
        # Try to find passed serial port: ------------------------------------------------------------------------------
        try:
            task_list = self._classification_task_dict[task[3]]
        # --------------------------------------------------------------------------------------------------------------
        except KeyError:
            # If passed unavailable serial port: -----------------------------------------------------------------------
            Error(where='fpga4p.core.Core._add_classify_queue()',
                  why=f'wrong serial port "{task[3]}" in task: {task}',
                  task_end=True)()
            # ----------------------------------------------------------------------------------------------------------
        else:  # Classification tasks are still not executed
            task_list.append(task)

    # ==================================================================================================================

    @staticmethod
    def _start_classify_queue(task_queue):
        """
        Start separate process for calculation of tasks queue with concrete FPGA.
        """
        for task in task_queue:  # This queue consists tasks for one concrete FPGA
            # Try to find passed classification class: -----------------------------------------------------------------
            try:
                classify_module = getattr(fpga4p.classify, task[1])
            # ----------------------------------------------------------------------------------------------------------
            except AttributeError:
                # If passed  classification class is unavailable: ------------------------------------------------------
                Error(where='fpga4p.core.Core._start_classify_queue()',
                      why=f'wrong classify class "{task[1]}" in task: {task}',
                      task_end=True)()
                # ------------------------------------------------------------------------------------------------------
            else:  # Start separate process for calculation of tasks queue with concrete FPGA
                classify_module.start_instance(task[0], task[2], task[3])

    # ==================================================================================================================


########################################################################################################################
# S E C O N D A R Y   C L A S S :  #####################################################################################
########################################################################################################################


class Notification:
    """
    Class for printing notifications.

    Args:
        self._string: Notification string.
        self._task_end: Notification about task ending.
        self._for_verbose: If notification for verbose mode only.
        self._time: Current time.
    """

    # ==================================================================================================================

    def __init__(self, where='unknown', what='unknown', task_end=False, for_verbose=False):
        # Special characters are declared in start.py
        self._time = None
        self._string = ('\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 +
                        f'\n{GREEN}{UNDERLINE_ON}NOTIFICATION{UNDERLINE_OFF}{RESET}' +
                        ' |{TIME}| :' +
                        f'\n\n\t{UNDERLINE_ON}Where?{UNDERLINE_OFF}: %s' % where +
                        f'\n\t{UNDERLINE_ON}What?{UNDERLINE_OFF}: %s' % what +
                        f'\n\t{UNDERLINE_ON}Task end?{UNDERLINE_OFF}: %s ' % task_end +
                        '\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 + '\n')
        self._task_end = task_end
        self._for_verbose = for_verbose

    # ==================================================================================================================

    def for_verbose(self):
        """
        Check if notification for verbose mode only.
        """
        return self._for_verbose

    # ==================================================================================================================

    def output(self):
        """
        Print notification string.
        """
        click.echo(self._string)

    # ==================================================================================================================

    def task_end(self):
        """
        Notification about task ending.
        """
        return self._task_end

    # ==================================================================================================================

    def __call__(self):
        """
        Send to the notification handler.
        """

        # Set current time: --------------------------------------------------------------------------------------------
        self._time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        self._string = self._string.format(TIME=self._time)
        # --------------------------------------------------------------------------------------------------------------
        Core().print_notification(self)

    # ==================================================================================================================


########################################################################################################################
# S E C O N D A R Y   C L A S S :  #####################################################################################
########################################################################################################################


class Error(Notification):
    """
    Class for printing errors.

    Args:
        self._string: Error string.
        self._for_verbose: Always False.
        self._fatal: If need to terminate notification handler.
    """

    # ==================================================================================================================

    def __init__(self, where='unknown', why='unknown', fatal=False, task_end=False):
        # Special characters are declared in start.py
        super().__init__(task_end=task_end)
        self._string = ('\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 +
                        f'\n{RED}{UNDERLINE_ON}ERROR{UNDERLINE_OFF}{RESET}' +
                        ' |{TIME}| :' +
                        f'\n\n\t{UNDERLINE_ON}Where?{UNDERLINE_OFF}: %s' % where +
                        f'\n\t{UNDERLINE_ON}Why?{UNDERLINE_OFF}: %s' % why +
                        f'\n\t{UNDERLINE_ON}Fatal?{UNDERLINE_OFF}: %s ' % fatal +
                        f'\n\t{UNDERLINE_ON}Task end?{UNDERLINE_OFF}: %s ' % task_end +
                        '\n\n' + f'{UNDERLINE_ON} {UNDERLINE_OFF}' * 40 + '\n')
        self._fatal = fatal

    # ==================================================================================================================

    def output(self):
        """
        Print error string.
        """
        click.echo(self._string)
        if self._fatal:
            exit(1)  # Exit from notification handler if error is fatal

    # ==================================================================================================================


########################################################################################################################
# S U P P O R T I N G   T O O L   F U N C T I O N :  ###################################################################
########################################################################################################################


def file_name_generator(task_name, extension, ending=''):
    """
    Generate file name for already existing file.
    """
    path = os.getcwd()
    counter = itertools.count(start=1)
    name = path + '/' + os.path.splitext(os.path.basename(task_name))[0]
    yield name + f'{ending}' + extension
    while True:
        yield name + f'{ending}' + f'_{counter.__next__()}' + extension


########################################################################################################################
# S U P P O R T I N G   T O O L   F U N C T I O N :  ###################################################################
########################################################################################################################


def get_byte_width(value):
    """
    Count byte size for variables in FPGA.
    """
    length = len(format(value, 'x'))
    if length % 2 == 0:
        return int(length / 2)
    else:
        return int((length + 1) / 2)


########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
