import os
import re
import numpy as np


def load(dataDirectory, dataModel, keepRealisations=False):
    """ Loading function for the COV-OBS model.  Also adds the data to the dataModel.

    :param dataDirectory: directory where the data is located
    :type dataDirectory: str (path)
    :param dataModel: Model to which the data should be added
    :type dataModel: Model
    :param keepRealisations: indicating if realisations should be kept or averaged (not used)
    :type keepRealisations: bool (default: False)
    :return: 0 if everything went well, -1 otherwise
    :rtype: int
    """

    # Reading measure BR and SV from covobs
    # List realisation
    for measureName in ["MF", "SV"]:

        realisations = []
        for file in os.listdir(dataDirectory):
            matchfile = re.match('^real(.*)_' + measureName.lower() + '_int_coefs.dat$', file)
            if matchfile is not None:
                realisations.append(os.path.join(dataDirectory, file))

        if len(realisations) == 0:
            print('No realisations were found while loading COV-OBS ! Aborting loading...')
            return -1

        g = None
        irealisation = 0
        # Storing realisation data in g
        for file in realisations:
            sourceData = np.loadtxt(file)
            times = sourceData[:, 0]
            sourceData = sourceData[:, 1:]

            # Initialisation of g (first iteration of the loop)
            if g is None:
                g = np.zeros((sourceData.shape[0], sourceData.shape[1], len(realisations)))
            g[:, :, irealisation] = sourceData
            irealisation += 1

        # Compute lmax from the size of the data previously read
        sizeData = np.where(sourceData[0] != 0)[0].shape[0] - 1
        lmax = (-2+np.sqrt(4+4*sizeData))/2

        if measureName == "SV":
            units = "nT/yr"
        if measureName == "MF":
            units = "nT"

        if keepRealisations:
            # If realisation must be kept, add the data to the model as read
            dataModel.addMeasure(measureName, measureName,
                                 lmax, units, g, times=times)
        else:
            # Else, average the data read on realisations
            dataModel.addMeasure(measureName, measureName,
                                 lmax, units,
                                 np.mean(g, axis=2), np.std(g, axis=2), times)
    return 0
