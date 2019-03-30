'''

catmatch project 
-------------------
File: cli.py

This file configures the Command line interface 

@author: R. THOMAS
@year: 2019
@place:  ESO
@License: GPL v3.0 - see LICENCE.txt
'''

#### Python Libraries
import argparse

class CLI:
    """
    This Class defines the arguments to be calle to use SPARTAN
    For the help, you can use 'catmatch -h' or 'catmatch --help'
    """
    def __init__(self,):
        """
        Class constructor, defines the attributes of the class
        and run the argument section
        """
        self.args()

    def args(self,):
        """
        This function creates defines the 4 main arguments of Catmatch using the argparse module
        """
        parser = argparse.ArgumentParser(description="specstack V1.2, R. Thomas, 2018, ESO, \
                This program comes with ABSOLUTELY NO WARRANTY; and is distributed under \
                the GPLv3.0 Licence terms.See the version of this Licence distributed along \
                this code for details.")

        parser.add_argument('file1', help="Your first catalog of data to match this is mandatory (positionnal argument)")

        parser.add_argument('file2', help="Your seconf catalog of data to match this is mandatory (positionnal argument)")

        parser.add_argument('column', help="The common column to match. The word you enter here must be in the header of the column you want to match and must be in the two catalogs")

        parser.add_argument('outputfile', help="The name of the output file that will be created (without spaces)")
        ##### GET the Arguments for SPARTAN startup
        self.arguments = parser.parse_args()


