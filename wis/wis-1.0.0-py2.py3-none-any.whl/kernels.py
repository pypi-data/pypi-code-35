# -----------------------------------------
# Third-party imports
# -----------------------------------------
import spiceypy as sp
import os
import warnings

# -----------------------------------------
# Local imports
# -----------------------------------------
from .satellite_obscodes import obscodeDict

# -----------------------------------------
# WIS functions & classes
# -----------------------------------------

class Manager(object):
    """
        Object to manage the download and loading of JPL spice-kernels
        
        Parameters
        ----------
        obscode : MPC observation code
            3 or 4 character string
        
        Attributes
        ----------
        ??? : ???
        ???
        
        Notes
        -----
        """
    
    def __init__(self, obscode=None):
        
        # Manage directory for downloaded kernels
        # -----------------------------------------------
        self.download_dir = self.define_download_dir()
        
        # If not called empty, do all subsequent steps
        # -----------------------------------------------
        if obscode != None:
            self.obscode = obscode
            
            # Manage sub-directory for obscode downloads
            # -----------------------------------------------
            self.download_subdir = self.define_download_subdir(self.obscode)
            
            # Try to get the local kernelFiles for satellite-specific kernels
            # If not available locally, do remote download of kernels
            # -----------------------------------------------
            I = obscodeDict[self.obscode]
            downloaded, kernelFiles = I.kernels_have_been_downloaded(self.download_subdir)
            if not downloaded:
                kernelFiles = I.download_data(self.download_subdir)

            # Load the satellite-specific kernels
            # -----------------------------------------------
            kernelFilepaths = [ os.path.join(self.download_subdir , f) for f in kernelFiles ]
            sp.furnsh(kernelFilepaths)




    def define_download_dir(self):
        """
        Returns the default path to the directory where files will be saved
        or loaded.

        By default, this method will return "~/.wispykernels" and create
        this directory if it does not exist.
        
        If the directory cannot be accessed or created, then it returns the local directory (".").
        
        N.B. Code "borrowed" from eleanor/targetData.py

        Returns
        -------
        download_dir : str
            Path to location of `download_dir` where kernels will be downloaded
        """
        download_dir = os.path.join(os.path.expanduser('~'), '.wispykernels')
        if os.path.isdir(download_dir):
            return download_dir
        else:
            # if it doesn't exist, make a new cache directory
            try:
                os.mkdir(download_dir)
            # downloads locally if OS error occurs
            except OSError:
                download_dir = '.'
                warnings.warn('Warning: unable to create {}. '
                              'Downloading TPFs to the current '
                              'working directory instead.'.format(download_dir))

        return download_dir

    def define_download_subdir(self, obscode):
        """
            Returns the default path to the subdirectory where files will be saved
            or loaded for a specific obscode
            
            Uses define_download_dir() to get its parent directly
            
            Returns
            -------
            download_subdir : str
                Path to location of `download_subdir` where kernels will be downloaded
                
        """
        # Get the main download-dir
        d = self.define_download_dir()
        # define a sub-dir path for this obscode
        download_subdir = os.path.join(d, obscode)
        if not os.path.isdir(download_subdir):
            os.mkdir(download_subdir)
        return download_subdir
