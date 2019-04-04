"""

Used  to manage and handle TLE files for the purpose of using them in STK.

"""

__author__ = "W. Conor McFerren"
__version__ = "0.0"
__maintainer__ = "W. Conor McFerren"
__email__ = "cnmcferren@gmail.com"


class TLE_Manager:
    
    """
    
    Class containing only static methods for processing TLE files.
    
    """
    
    @staticmethod
    def ParseTLE(filename):
    
        """
        
        Parses a TLE file of the given file name.
        
        Parameters:
            filename (str): Name of the TLE file.
            
            """
    
        #Create array for return value
        outputArray = []
    
        #Open TLE file and burn first line (that contains name of satellite)
        tle = open(filename,'r')
        tle.readline()
    
        #Saves first and second lines to variables
        firstLine = tle.readline()
        secondLine = tle.readline()
    
        #Adds line to output array
        outputArray.append(firstLine)
        outputArray.append(secondLine)
    
        #Close tle file
        tle.close()
    
        return outputArray

    @staticmethod
    def RetrieveTLE(self):
    
        """
    
        INCOMPLETE
    
        """
    
        ##TODO Implement method to return specific TLE from STK database
        return 0