from sklearn_helper.data.data_cleaner import DataCleaner


class DummyCleaner(DataCleaner):
    def clean_training_data(self, x, y):
        return x, y

    def clean_testing_data(self, x):
        return x
