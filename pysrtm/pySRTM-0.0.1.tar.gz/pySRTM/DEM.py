# -*- coding: utf-8 -*-
"""
Authors: Tim Hessels
Module: Collect/SRTM
"""
import os
import shutil
from pySRTM.DataAccess import DownloadData
import sys


def main(Dir, latlim, lonlim, Waitbar = 1):
    """
    Downloads HydroSHED data from http://srtm.csi.cgiar.org/download

    this data includes a Digital Elevation Model (DEM)
    The spatial resolution is 90m (3s)

    The following keyword arguments are needed:
    Dir -- 'C:/file/to/path/'
    latlim -- [ymin, ymax]
    lonlim -- [xmin, xmax]
    Waitbar -- '1' if you want a waitbar (Default = 1)
    """

    # Create directory if not exists for the output
    output_folder = os.path.join(Dir, 'SRTM', 'DEM')
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the output map and create this if not exists
    nameEnd = os.path.join(output_folder, 'DEM_SRTM_m_3s.tif')

    if not os.path.exists(nameEnd):

        # Create Waitbar
        if Waitbar == 1:
            print('\nDownload SRTM altitude map with a resolution of 3s')
            total_amount = 1
            amount = 0
            printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)

        # Download and process the data
        trash_folder = DownloadData(output_folder, latlim, lonlim)

        # Delete the temporary folder
        try:
            shutil.rmtree(trash_folder)
        except:
            pass
        
        if Waitbar == 1:
            amount = 1
            printWaitBar(amount, total_amount, prefix = 'Progress:', suffix = 'Complete', length = 50)

    else:
        if Waitbar == 1:
            print("\nSRTM altitude map (3s) already exists in output folder")

def printWaitBar(i, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    This function will print a waitbar in the console

    Variables:

    i -- Iteration number
    total -- Total iterations
    fronttext -- Name in front of bar
    prefix -- Name after bar
    suffix -- Decimals of percentage
    length -- width of the waitbar
    fill -- bar fill
    """
    import sys
    import os

    # Adjust when it is a linux computer
    if (os.name=="posix" and total==0):
        total = 0.0001

    percent = ("{0:." + str(decimals) + "f}").format(100 * (i / float(total)))
    filled = int(length * i // total)
    bar = fill * filled + '-' * (length - filled)

    sys.stdout.write('\r%s |%s| %s%% %s' %(prefix, bar, percent, suffix))
    sys.stdout.flush()

    if i == total:
        print()

if __name__ == '__main__':
    main(sys.argv)

