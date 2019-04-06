"""
    Functions and Objects used by WIS to download
    data (spice-kernels) for specified 
    satellite missions
    
    Each Instruction-Object is saved into an overall
    obscodeDict
     - The keys defines the set of obscodes that the user can expect to return sensible results
     - The values defines the Instructions-Object that the user can use to download kernels

"""
# -----------------------------------------
# Third-party imports
# -----------------------------------------
from bs4 import BeautifulSoup
import requests
import glob
import wget
import numpy as np
import sys

# -----------------------------------------
# WIS functions & classes
# -----------------------------------------

class Instructions(object):
    """
        Instruction-Object
        
        Holds the specification of where data is online
        
        Provides method to download the data to local machine
    """
    def download_data(self, destinationDirectory):
        
        # Download explicitly named files
        for f in self.files:
            try:
                wget.download(f, out=destinationDirectory)
            except:
                print("Failed to download %r" % f)
                    
        # Download files using wildcards
        for url,wildcard in self.wildcards.items():
            for f in self._listFD(url, wildcard = wildcard):
                wget.download(f, out=destinationDirectory)
            
    
        # Check whether the download worked
        downloaded, downloadedKernelFiles = self.kernels_have_been_downloaded(destinationDirectory)

        if downloaded:
            return downloadedKernelFiles
        else:
            #print("destinationDirectory", destinationDirectory)
            #print("downloaded, downloadedKernelFiles", downloaded, downloadedKernelFiles)
            sys.exit('download unsuccessful ... ')
            

    def kernels_have_been_downloaded(self, destinationDirectory):
        
        # Check what files exist locally
        # -----------------------------------------------
        downloadedKernelFiles = [ f[f.rfind("/")+1:] for f in glob.glob("%s/*" % destinationDirectory) ]
        
        # Check what files *need* to exist (if wildcards exist, we demand at least 1 download per wildcard)
        # - if they don't, then download
        # -----------------------------------------------
        requiredFiles = [ f[f.rfind("/")+1:] for f in self.files ]
        if len(downloadedKernelFiles) < len(requiredFiles)+len(self.wildcards) or \
                not np.all( [ rf in downloadedKernelFiles for rf in requiredFiles] ):
            return False, []
        else:
            return True, downloadedKernelFiles


    def _listFD(self , url, wildcard=''):
        '''
            List all the files in a url
            Allows a wildcard of the form stem*end
            Stolen from 
            https://stackoverflow.com/questions/11023530/python-to-list-http-files-and-directories
        '''
        
        # Split wildcard (if it contains "*")
        if wildcard.count("*") == 0:
            wildcardStart = wildcard
            wildcardEnd   = ''
        elif wildcard.count("*") == 1:
            wildcardStart = wildcard[ : wildcard.find("*")]
            wildcardEnd   = wildcard[ wildcard.find("*") + 1 :]
        else:
            sys.exit('Cannot parse wildcards with >=2 asterisks in them ... [%r]' % wildcard)

        # Get page ...
        page = requests.get(url).text

        # Parse page
        soup = BeautifulSoup(page, 'html.parser')
        
        # Return matching filenames
        return [url + '/' + node.get('href') for node in soup.find_all('a') if node.get('href').startswith(wildcardStart) and node.get('href').endswith(wildcardEnd) ]



# Define the location of the kernels to download for TESS
# --------------------------------------------------------------------------
TESS = Instructions()
TESS.obscode        = '-95'
TESS.name           = 'TESS'
TESS.files          = ['https://archive.stsci.edu/missions/tess/models/tess2018338154046-41240_naif0012.tls',
                       'https://archive.stsci.edu/missions/tess/models/tess2018338154429-41241_de430.bsp']
TESS.wildcards      = {'https://archive.stsci.edu/missions/tess/models/':'TESS_EPH_DEF*'}

                       
# Define the location of the kernels to download for K2
# --------------------------------------------------------------------------
K2 = Instructions()
K2.obscode          = '-227'
K2.name             = 'K2'
K2.files            = ['https://archive.stsci.edu/pub/k2/spice/kplr2018134232543.tsc',
                       'https://archive.stsci.edu/pub/k2/spice/naif0012.tls',
                       'https://archive.stsci.edu/pub/k2/spice/spk_2018290000000_2018306220633_kplr.bsp']
K2.wildcards        = {}


# Define the location of the kernels to download for CASSINI
# --------------------------------------------------------------------------
CASSINI = Instructions()
CASSINI.obscode          = '-82'
CASSINI.name             = 'CASSINI'
CASSINI.files            = ['https://naif.jpl.nasa.gov/pub/naif/generic_kernels/lsk/a_old_versions/naif0009.tls',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/sclk/cas00084.tsc',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/pck/cpck05Mar2004.tpc',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/fk/release.11/cas_v37.tf',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ck/04135_04171pc_psiv2.bc',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/030201AP_SK_SM546_T45.bsp',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/ik/release.11/cas_iss_v09.ti',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/020514_SE_SAT105.bsp',
                           'https://naif.jpl.nasa.gov/pub/naif/CASSINI/kernels/spk/981005_PLTEPH-DE405S.bsp']
CASSINI.wildcards        = {}



# Define a handy dictionary containing all of the defined Instruction-Objects
# --------------------------------------------------------------------------
obscodeDict = {I.obscode:I for I in [TESS, K2, CASSINI]}

