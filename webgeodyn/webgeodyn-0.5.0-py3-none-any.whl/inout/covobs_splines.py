import os
import glob
import numpy as np
from scipy.signal import bspline


def build_gnm_from_file(file_name, dt=0.5):
    """
    Builds gnm from the spline coeffs stored in a file. The timestep of the resulting dates can be changed.

    :param file_name: Name of the file where the spline coeffs are stored
    :type file_name: str
    :param dt: Timestep of the evaluation dates (default: 0.5)
    :type dt: float
    :return: evaluation dates and the reconstructed gnm at these dates
    :rtype: np.array (dim: n_dates), np.array (dim: n_dates x n_gnm)
    """
    center_dates, spl_coeffs, spl_order, knot_sp = read_spline_coeffs_file(file_name)
    eval_dates = np.arange(center_dates[spl_order//2+1], center_dates[-spl_order//2-1], dt)
    return build_gnm_from_spline_coeffs(eval_dates, center_dates, spl_coeffs, spl_order)


def eval_spline(date_to_eval, center_date, spl_order, knot_spacing):
    """ Evaluates a spline at date_to_eval.
    The spline is of order spl_order, spacing knot_spacing and centered on center_date."""
    normalised_X = (date_to_eval - center_date) / knot_spacing
    return bspline(normalised_X, spl_order)


def get_date_indexes_for_spl_eval(eval_date, spl_dates, spl_order):
    """ Returns the indexes of the dates of spl_dates needed to evaluate the value at eval_date."""
    eval_date_index = np.searchsorted(spl_dates, eval_date)
    return np.arange(eval_date_index - spl_order//2 - 1, eval_date_index + spl_order//2 + 1)


def build_gnm_from_spline_coeffs(dates_for_eval, spl_dates, spl_coeffs, spl_order, debug=False):
    """
    Builds the gnm from the spline coeffs and the parameters of splines (center_dates, order, spacing).
    This method tries to evaluate only the needed splines at the evaluation dates.

    :param dates_for_eval:
    :type dates_for_eval:
    :param spl_dates:
    :type spl_dates:
    :param spl_coeffs:
    :type spl_coeffs:
    :param spl_order:
    :type spl_order:
    :param debug:
    :type debug:
    :return:
    :rtype:
    """
    n_spl_dates, Nb = spl_coeffs.shape
    assert n_spl_dates == spl_dates.shape[0]
    knot_spacing = spl_dates[1] - spl_dates[0]

    gnm = np.zeros((len(dates_for_eval), Nb))
    for i_date, eval_date in enumerate(dates_for_eval):
        date_indexes = get_date_indexes_for_spl_eval(eval_date, spl_dates, spl_order)
        for j in date_indexes:
            center_date = spl_dates[j]
            spl_value = eval_spline(eval_date, center_date, spl_order, knot_spacing)
            if debug:
                print('{}: evaluating spline at {} - Coef : {} - Value: {}'.format(eval_date, center_date, spl_coeffs[j, 0], spl_value))
            gnm[i_date] += spl_coeffs[j]*spl_value
        if debug: print('------')
    return dates_for_eval, gnm


def build_gnm_from_spline_coeffs_all_splines(dates_for_eval, spl_dates, spl_coeffs, spl_order, debug=False):
    """
    Builds the gnm from the spline coeffs and the parameters of splines (center_dates, order, spacing).
    This method evaluates *all* splines for any date.

    :param dates_for_eval:
    :type dates_for_eval:
    :param spl_dates:
    :type spl_dates:
    :param spl_coeffs:
    :type spl_coeffs:
    :param spl_order:
    :type spl_order:
    :param debug:
    :type debug:
    :return:
    :rtype:
    """
    n_spl_dates, Nb = spl_coeffs.shape
    gnm = np.zeros((len(dates_for_eval), Nb))
    # assert spl_dates.shape[0] == n_dates
    knot_spacing = spl_dates[1] - spl_dates[0]
    for i_date, eval_date in enumerate(dates_for_eval):
        for j, center_date in enumerate(spl_dates):
            spl_value =  eval_spline(eval_date, center_date, spl_order, knot_spacing)
            if debug:
                print('{}: evaluating spline at {} - Coef : {} - Value: {}'.format(eval_date, center_date, spl_coeffs[j, 0], spl_value))
            gnm[i_date] += spl_coeffs[j]*spl_value
        if debug: print('------')
    return dates_for_eval, gnm


def read_spline_coeffs_file(file_name):
    """
    Extracts the spline coeffs and the spline parameters from a file

    :param file_name: name of the spline coeffs file
    :type file_name: str
    :return: center dates, spline coeffs, spline order and knot spacing
    :rtype: np.array, np.array, int, float
    """
    with open(file_name) as f:
        f.readline()  # Skip header with mod name
        header = f.readline().split()
        # Read info
        Lb = int(header[0])
        if Lb == 1:
            Nb = 1  # External field has only one coeff (q10)
        else:
            Nb = Lb * (Lb + 2)
        n_dates = int(header[1])
        spl_order = int(header[2])
        center_dates = np.array(header[3:][spl_order // 2:-spl_order // 2], dtype=float)
        knot_sp = center_dates[1] - center_dates[0]
        # Create the list of coeffs and append the coeffs to it
        read_spl_coeffs = []
        for line in f:
            line_coeffs = line.split()
            read_spl_coeffs.extend(line_coeffs)

    spl_coeffs = np.array(read_spl_coeffs, dtype=np.float64)
    spl_coeffs = spl_coeffs.reshape((n_dates, Nb))
    return center_dates, spl_coeffs, spl_order, knot_sp


def load(dataDirectory, dataModel, keepRealisations=False):
    """ Loading function for splines files (COV-OBS-like).  Also adds the data to the dataModel.

    :param dataDirectory: directory where the data is located
    :type dataDirectory: str (path)
    :param dataModel: Model to which the data should be added
    :type dataModel: Model
    :param keepRealisations: indicating if realisations should be kept or averaged (not used)
    :type keepRealisations: bool (default: False)
    :return: 0 if everything went well, -1 otherwise
    :rtype: int
    """

    for measureName in ["MF"]:
        generic_model_path = os.path.join(dataDirectory, 'mod*')
        model_files = glob.glob(str(generic_model_path))
        if len(model_files) == 0:
            print('No spline files were found in {} ! Aborting loading...'.format(dataDirectory))
            return -1

        # Load the latest model in the directory
        model_files.sort(reverse=True)
        print(os.path.basename(model_files[0]))
        times, gnm = build_gnm_from_file(model_files[0])
        Nb = gnm.shape[1]
        Lb = np.sqrt(Nb+1) - 1
        lmax = int(Lb)
        # Assert that Nb gives an integer Lb
        assert Lb == lmax

        if measureName == "SV":
            units = "nT/yr"
        if measureName == "MF":
            units = "nT"

        dataModel.addMeasure(measureName, measureName, lmax, units, gnm, times=times)

    return 0
