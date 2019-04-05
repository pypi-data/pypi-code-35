########################################################################################################################
# M O D U L E   D O C U M E N T A T I O N : ############################################################################
########################################################################################################################


"""
The entry point of "fpga4p".

This module contains the entry point of the application. It also contains
attributes for highlighting text displayed in the terminal.

Example:
    This example starts the training task:

        $ python3 start.py --trn "training.csv,train_nbc"

    This example starts the classification task:

        $ python3 start.py --cls "classification.csv,classify_nbc,training.wd,/dev/ttyUSB0"

    This example prints available modules for training and classification,
    as well as available serial USB ports:

        $ python3 start.py --info

    For more information about the format of the arguments, use the parameter "--help"

Attributes:
    UNDERLINE_ON: Enable underline for string output to terminal.
    UNDERLINE_OFF: Disable underline for string output to terminal.
    GREEN: Enable green font for string output to terminal.
    RED: Enable red font for string output to terminal.
    RESET: Disable color font for string output to terminal.
"""


########################################################################################################################
# I M P O R T :  #######################################################################################################
########################################################################################################################


import fpga4p
import click
import os
import colorama
import serial.tools.list_ports


########################################################################################################################
# S P E C I A L   C H A R A C T E R S   F O R   T E R M I N A L : ######################################################
########################################################################################################################


# Characters for special output in the terminal: -----------------------------------------------------------------------
UNDERLINE_ON = '\u001b[4m'
UNDERLINE_OFF = '\u001b[0m'
GREEN = colorama.Fore.LIGHTGREEN_EX
RED = colorama.Fore.LIGHTRED_EX
RESET = colorama.Style.RESET_ALL
# ----------------------------------------------------------------------------------------------------------------------


########################################################################################################################
# E N T R Y   P O I N T :  #############################################################################################
########################################################################################################################


# Declaration of the entry point for terminal call: --------------------------------------------------------------------
@click.command()
# ----------------------------------------------------------------------------------------------------------------------
# Declaration of the arguments for terminal call: ----------------------------------------------------------------------
@click.option('--trn', default=None,
              help=('["training_file_1.csv,training_algorithm_1;...;'
                    'training_file_N.csv,training_algorithm_N"]'))
@click.option('--cls', default=None,
              help=('["classification_file_1.csv,classification_algorithm_1,word_dict_1.wd,usb_device_1;...;'
                    'classification_file_N.csv,classification_algorithm_N,word_dict_N.wd,usb_device_N"]'))
@click.option('-v', is_flag=True, help='Verbose mode.')
@click.option('--info', is_flag=True, help='Print information about'
                                           ' available algorithms for training and classification and'
                                           ' available serial USB ports.')
# ----------------------------------------------------------------------------------------------------------------------
def entry_point(trn: str, cls: str, v: bool, info: bool):
    # Output for "--help" option: --------------------------------------------------------------------------------------
    """
    MANUAL:

    Training opportunities:

        1) Training tasks executes in parallel processes.

        2) Each training task generates: ".sv" file for FPGA, ".wd" file
         and ".tar" archive with model data for prospective
             classification task.


    Training specialities:

        1) "training_file.csv" must contain classes in the first column.

        2) "training_file.csv" must not contain a column head.

        3) The character - separator of "training_file.csv" must be ",".

        4) You can check available training algorithms with option "--info".


    Classification opportunities:

        1) Classification tasks might be executed parallel on several FPGAs.

        2) Several classification tasks, addressed to FPGA, execute consistently.

        3) Each classification task generates ".csv" file with predicted answers.


    Classification specialities:

        1) "classification_file.csv" must not contain a column head.

        2) The character - separator of "training_file.csv" must be ",".

        3) The "word_dict.wd" might match to firmware of FPGA.

        4) You can check available training algorithms and USB serial ports
            with option "--info".

    Examples:

         1) This example starts the training task:

            $ fpga4p --trn "training.csv,train_nbc"

        2) This example starts the classification task:

            $ fpga4p --cls "class.csv,classify_nbc,training.wd,/dev/ttyUSB0"

        3) This example prints available modules for training and
            classification, as well as available serial USB ports:


            $ fpga4p --info
    """
    # ------------------------------------------------------------------------------------------------------------------

    # If "--info" flag was given: --------------------------------------------------------------------------------------
    if info:
        # Print all available training algorithms: ---------------------------------------------------------------------
        click.echo(f'\n{UNDERLINE_ON}Available training algorithms{UNDERLINE_OFF}: ')
        for train_module in dir(fpga4p.train):
            if 'train_' in train_module:
                click.echo(f'\n\t "{train_module}"')
        # --------------------------------------------------------------------------------------------------------------

        # Print all available classification algorithms: ---------------------------------------------------------------
        click.echo(f'\n{UNDERLINE_ON}Available classification algorithms{UNDERLINE_OFF}: ')
        for classify_module in dir(fpga4p.classify):
            if 'classify_' in classify_module:
                click.echo(f'\n\t "{classify_module}"')
        # --------------------------------------------------------------------------------------------------------------

        # Print all available serial USB ports: ------------------------------------------------------------------------
        click.echo(f'\n{UNDERLINE_ON}Available serial USB ports{UNDERLINE_OFF}: ')
        for serial_port in serial.tools.list_ports.comports():
            click.echo(f'\n\t "{serial_port}"')
        # --------------------------------------------------------------------------------------------------------------
        return 0
    # ------------------------------------------------------------------------------------------------------------------

    # If "--info" flag was not given: ----------------------------------------------------------------------------------
    elif cls is not None:
        # Print notification about ROOT rights: ------------------------------------------------------------------------
        click.echo(f'\n{UNDERLINE_ON}FPGA4P needs ROOT rights for communication with serial ports:{UNDERLINE_OFF}\n')
        # --------------------------------------------------------------------------------------------------------------

        # Request ROOT rights in the terminal: -------------------------------------------------------------------------
        fail = os.system('sudo echo')
        if not fail:
            click.echo(f'\n{GREEN}{UNDERLINE_ON}ROOT rights obtained!{RESET}')
        else:
            click.echo(f'\n{RED}{UNDERLINE_ON}ROOT rights did not obtain!{RESET}')
            click.echo(f'\n{RED}Classification tasks will not be executed!{RESET}')
            cls = None
        # --------------------------------------------------------------------------------------------------------------

    # Start the core module: -------------------------------------------------------------------------------------------
    core = fpga4p.core.Core()
    core.set_kwargs(trn, cls, v)
    core.start()
    # ------------------------------------------------------------------------------------------------------------------

# ======================================================================================================================


if __name__ == '__main__':
    entry_point()

# ======================================================================================================================


########################################################################################################################
# E N D   O F   F I L E .  #############################################################################################
########################################################################################################################
