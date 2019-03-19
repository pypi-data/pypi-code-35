from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, f1_score

class Evaluator:

    def __init__(self, metric='f1', model='LR', score=None):
        self.metric = metric
        self.model = model
        self.score = score

    def fit_score(self, df, target):
        labelEncoder = LabelEncoder()
        for col in df.columns:
            df[col] = labelEncoder.fit_transform(df[col].astype(str))

        train, test = train_test_split(df, test_size=0.2)
        train_y = train[self.target]
        train_X = train[[x for x in df.columns if self.target not in x]]

        test_y = test[self.target]
        test_X = test[[x for x in df.columns if self.target not in x]]

        if self.model == 'LR':
            clf = LogisticRegression()


