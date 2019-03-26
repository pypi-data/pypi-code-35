from sklearn.metrics import confusion_matrix


def true_positive_rate(y_true, y_pred):
    _, _, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return tp/(tp + fn)


def fmr_score(y_true, y_pred):
    """
    Function to compute FMR metric (FP/(FP + TN))
    (False match rate - FMR, also called FAR = False Accept Rate)

    :param y_true: ground truth (correct) target values
    :param y_pred: estimated targets as returned by a classifier
    :return: fraction of incorrectly accepted samples
    """

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fp/(fp + tn)


def fnmr_score(y_true, y_pred):
    """
    Function to compute FNMR metric (FN/(TP + FN))
    (False non-match rate - FNMR, also called FRR = False Reject Rate)

    :param y_true: ground truth (correct) target values
    :param y_pred: estimated targets as returned by a classifier
    :return: fraction of incorrectly rejected samples
    """

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
    return fn/(tp + fn)


def hter_score(y_true, y_pred):
    """
    Function to compute HTER metric ((FMR + FNMR)/2)

    :param y_true: ground truth (correct) target values
    :param y_pred: estimated targets as returned by a classifier
    :return: return average of FMR and FNMR
    """

    return (fmr_score(y_true, y_pred) + fnmr_score(y_true, y_pred))/2
