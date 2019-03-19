import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, f1_score



class Analyze:

    def __init__(self, file, target):
        self.file = file
        self.target = target



    def read_data(self, index_col=None):
        if self.file.split('.')[-1] == 'csv':
            # if isinstance(index_col, str):
            df = pd.read_csv(self.file, index_col=index_col)

            return df


    def describe_data(self, df):
        row_num, col_num = df.shape
        # print (row_num, col_num)
        col_list = df.columns.tolist()
        # print (col_list)
        col_dict = {}
        # print (df['Sex'].unique().tolist())
        for col in col_list:
            if df[col].dtypes == 'object':
                col_dict[col] = df[col].dropna().unique().tolist()
            elif df[col].dtypes == 'int64':
                col_dict[col] = [df[col].min(), df[col].max(), 'int64']
            elif df[col].dtypes == 'float64':
                col_dict[col] = [df[col].min(), df[col].max(), 'float64']
            else:
                pass
        # print (col_dict)
        # print (df['Sex'].dtypes)
        return col_dict, row_num

    # def predict(self, df):
    #     labelEncoder = LabelEncoder()
    #     for col in df.columns:
    #         df[col] = labelEncoder.fit_transform(df[col].astype(str))
    #
    #     train, test = train_test_split(df, test_size=0.2)
    #     train_y = train[self.target]
    #     train_X = train[[x for x in df.columns if self.target not in x]]
    #
    #     test_y = test[self.target]
    #     test_X = test[[x for x in df.columns if self.target not in x]]
    #
    #     models = [LogisticRegression()]
    #     model_names = ['Logistic Regression']
    #     for i, model in enumerate(models):
    #         model.fit(train_X, train_y)
    #         print('The accurancy of ' + model_names[i] + ' is ' + str(accuracy_score(test_y, model.predict(test_X))))

    def read_analyze(self):
        self.read_data()

# ana = Analyze('Risk')
# df = ana.read_data('german_credit_data.csv', 0)
# ana.describe_data(df)
# ana.predict(df)