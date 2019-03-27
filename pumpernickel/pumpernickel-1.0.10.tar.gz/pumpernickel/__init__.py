# coding:utf-8

# from .matrix import Matrix
# def p(a):
#     display(a)
# def pa(a):
#     pd.set_option('display.max_rows', 50)
#     display(a)
#     pd.set_option('display.max_rows', 5)
# def ph(a):
#     display(a.head())
# def pt(a):
#     pp(type(a))
# def ps(a):
#     pp(a.shape)
# def pr(a):
#     sys.stdout.write("\r{}".format(a))
#     sys.stdout.flush()

# class Matrix:
#     def __init__(self):
#         print('init')
#     def hoge():
#         print('hoge')


from IPython.core.display import display
def p(a):
    display(a)

class pn:
    def print_confusion_matrix(y_valid, y_pred):
        from sklearn import metrics
        import numpy as np, pandas as pd
        import matplotlib.pyplot as plt, seaborn as sns
        plt.rcParams['font.family'] = 'IPAPGothic'

        labels = sorted(list(set(y_valid)))
        cmx_data = metrics.confusion_matrix(y_valid, y_pred, labels=labels)
        df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
        plt.figure()
        sns.heatmap(df_cmx, annot=True)
        plt.show()

    def print_evaluation(y_valid, y_pred, average='binary'):
        from sklearn import metrics
        print("accuracy : %f" % metrics.accuracy_score(y_valid, y_pred))
        print("precision: %f" % metrics.precision_score(y_valid, y_pred, average=average))
        print("recall   : %f" % metrics.recall_score(y_valid, y_pred, average=average))
        print("f1       : %f" % metrics.f1_score(y_valid, y_pred, average=average))
        if average == 'binary':
            fpr, tpr, _ = metrics.roc_curve(y_valid, y_pred)
            print("auc      : %f" % metrics.auc(fpr, tpr))

    def print_auc_plot(y_valid, y_pred):
        from sklearn import metrics
        import matplotlib.pyplot as plt, seaborn as sns
        plt.rcParams['font.family'] = 'IPAPGothic'

        fpr, tpr, _ = metrics.roc_curve(y_valid, y_pred)
        plt.figure()
        plt.plot(fpr, tpr, label='ROC curve (area = %.2f)' % metrics.auc(fpr, tpr))
        plt.legend()
        plt.title('ROC curve')
        plt.xlabel('FPR')
        plt.ylabel('TPR')
        return metrics.auc(fpr, tpr)

    def print_feature_importance(columns, model):
        import pandas as pd
        df = pd.DataFrame(index=columns)
        df["feature_importances"] = model.feature_importances_.round(6)
        df = df.sort_values('feature_importances', ascending=False)
        return df['feature_importances']

    def print_coef(columns, model):
        import pandas as pd
        df = pd.DataFrame(index=columns)
        df['coef'] = model.coef_[0].round(6)
        df = df.sort_values('coef', ascending=False)
        return df['coef']



