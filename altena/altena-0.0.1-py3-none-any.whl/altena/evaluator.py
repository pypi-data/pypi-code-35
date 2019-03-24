from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import average_precision_score
from sklearn.metrics import precision_recall_curve
import matplotlib.pyplot as plt


def calc_metrics(y_true, y_proba, y_proba_neg, save_curve_filepath=None):

    y_pred = (y_proba >= y_proba_neg) * 1

    # PR曲線
    precisions, recalls, th = precision_recall_curve(y_true, y_proba)
    ap = average_precision_score(y_true, y_proba)

    # PR曲線をプロット
    if save_curve_filepath is not None:
        plt.plot(recalls, precisions, label='PR curve (area = %.3f)' % ap)
        plt.legend()
        plt.title('PR curve')
        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.grid(True)
        plt.savefig(save_curve_filepath)

    conf_matrix = confusion_matrix(y_true, y_pred)
    acc = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    metrics = {
        'confusion_matrix': conf_matrix,
        'ap': ap,
        'accuracy': acc,
        'precision': precision,
        'recall': recall,
        'F1': f1
    }
    return metrics
