"""

    .. note: This module provides functions to read/convert miPod data.

    .. moduleauthor: Dominik Schuldhaus <schuldhaus.dominik@gmail.com>

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

def importMiPodCSV(file):

    # load csv file
    tmp = pd.read_csv(file, delimiter=',', header=None)

    # convert to matrix
    data = tmp.values

    # get accelerometer
    acc = data[:, 1:4]

    # get gyroscope
    gyr = data[:, 5:8]

    return acc, gyr

def main():

    # import mipod data
	acc, gyr = importMiPodCSV(sys.argv[1])

	# plot signal
	fig = plt.figure(num=sys.argv[1])

	ax1 = plt.subplot(211)
	plt.plot(acc)
	plt.ylabel('Linear acceleration [m/s^2]')

	ax2 = plt.subplot(212, sharex=ax1)
	plt.plot(gyr)
	plt.ylabel('Angular velocity [s]')

	plt.show()

if __name__ == "__main__":
    
    main()