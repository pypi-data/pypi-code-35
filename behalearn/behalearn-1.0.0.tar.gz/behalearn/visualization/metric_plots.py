from matplotlib import pyplot as plt
import numpy as np
from behalearn.metrics import fmr_score, fnmr_score, true_positive_rate


def trapezoid_diagonal_intersection(A, B, C, D):
    """
    Calculates coordinates of point which is intersection of trapezoid
    diagonal. Trapezoid bases are lines BC and AD.

    :param A: point A (tuple) of trapezoid
    :param B: point B (tuple) of trapezoid
    :param C: point C (tuple) of trapezoid
    :param D: point D (tuple) of trapezoid
    :return: threshold, EER value; coordinates of diagonal intersection
    """
    A_x, A_y = A
    _, B_y = B
    C_x, C_y = C
    _, D_y = D
    bc = abs(A_y - B_y)
    ad = abs(C_y - D_y)
    bd = np.sqrt(((C_y - A_y) ** 2) + ((C_x - A_x) ** 2))

    ratio = bc / ad

    x = bd / (ratio + 1)

    dx = (x / bd) * abs(C_x - A_x)
    dy = (x / bd) * abs(C_y - A_y)

    return C_x + dx, C_y - dy


def calc_err(thresholds, fmrs, fnmrs):
    """
    Calculates EER and threshold value where it appears.

    :param thresholds: array of thresholds
    :param fmrs: array of FAR errors corresponding to threshold
    :param fnmrs: array of FRR errors corresponding to threshold
    :return: threshold, eer
    """
    for i in range(len(fmrs)):
        if fmrs[i] == fnmrs[i]:
            return thresholds[i], fmrs[i]
        if fnmrs[i] > fmrs[i]:
            return trapezoid_diagonal_intersection(
                (thresholds[i], fmrs[i]),
                (thresholds[i], fnmrs[i]),
                (thresholds[i-1], fmrs[i-1]),
                (thresholds[i-1], fnmrs[i-1])
            )


def plot_far_frr_eer(data, thresholds):
    """
    Plots FAR, FRR and EER for each user dataframe was trained for

    :param data: DataFrame containing columns: user_train, proba1 & y_test
    :param thresholds: array of thresholds
    :return:
    """
    tested_users = data.user_train.unique()

    for t_user in tested_users:
        fmrs = []
        fnmrs = []
        t_user_data = data[data.user_train == t_user]
        for threshold in thresholds:
            y_pred_thr = \
                t_user_data.proba1.apply(lambda x: 1 if x > threshold else 0)
            fmrs.append(fmr_score(t_user_data.y_test, y_pred_thr))
            fnmrs.append(fnmr_score(t_user_data.y_test, y_pred_thr))
        eer_thr, err = calc_err(thresholds, fmrs, fnmrs)

        plt.figure(str(t_user))
        plt.plot(thresholds, fmrs, 'r-')
        plt.plot(thresholds, fnmrs, 'b-')
        plt.plot(eer_thr, err, 'go')

    plt.show()


def plot_det_curve(data, thresholds, scale_log):
    """
        Plots DET curve with EER point for each user dataframe was trained for

        :param data: DataFrame containing columns: user_train, proba1 & y_test
        :param thresholds: array of thresholds
        :return:
        """
    tested_users = data.user_train.unique()

    for t_user in tested_users:
        fmrs = []
        fnmrs = []
        t_user_data = data[data.user_train == t_user]
        for threshold in thresholds:
            y_pred_thr = \
                t_user_data.proba1.apply(lambda x: 1 if x > threshold else 0)
            fmrs.append(fmr_score(t_user_data.y_test, y_pred_thr))
            fnmrs.append(fnmr_score(t_user_data.y_test, y_pred_thr))
        eer_thr, err = calc_err(thresholds, fmrs, fnmrs)

        plt.figure(str(t_user))
        plt.plot(fmrs, fnmrs, '-r')
        plt.plot(err, err, 'go')
        plt.xlabel('fmrs - FAR')
        plt.ylabel('fnmrs - FRR')
        if scale_log:
            plt.xscale('log')
            plt.yscale('log')
        else:
            plt.plot([0, 0.5, 1], [0, 0.5, 1], ':k')

    plt.show()


def plot_roc_curve(data, thresholds):
    """
    Plots ROC curve for each user dataframe was trained for

    :param data: DataFrame containing columns: user_train, proba1 & y_test
    :param thresholds: array of thresholds
    :return:
    """

    tested_users = data.user_train.unique()

    for t_user in tested_users:
        true_positive_rates = []
        false_match_rates = []
        t_user_data = data[data.user_train == t_user]
        for threshold in thresholds:
            y_pred_thr = \
                t_user_data.proba1.apply(lambda x: 1 if x > threshold else 0)
            true_positive_rates.append(true_positive_rate(t_user_data.y_test,
                                                          y_pred_thr))
            false_match_rates.append(fmr_score(t_user_data.y_test, y_pred_thr))

        plt.figure(str(t_user))
        plt.plot(false_match_rates, true_positive_rates, 'b-')

    plt.show()
