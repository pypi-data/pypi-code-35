import numpy as np
from functools import partial
from sklearn_helper.data.data_cleaner import DataCleaner


class FeatureEngineeringDataCleaner(DataCleaner):
    """
    If you want to know a bit more about the logic behind this logic
    visit https://www.kaggle.com/andresarrieche7/house-prices-advanced-regression-score-0-13493/
    """

    def clean_training_data(self, df, y):
        df = self.general_cleanup(df)
        df = self.filter_numerical_data_for_training(df)
        sale_price = df["SalePrice"]
        df = df.drop(["Id", "SalePrice"], 1)
        return df, np.log(sale_price)

    def clean_testing_data(self, df):
        df = self.general_cleanup(df)

        df = df.drop(["Id"], 1)
        if "SalePrice" in df.columns.values:
            df = df.drop(["SalePrice"], 1)
        return df

    def general_cleanup(self, df):
        df = df.copy()

        df = df.fillna(0)
        df = self.transform_data(df)
        df = self.transform_numerical_data(df)
        df = self.remove_unused_features(df)
        return df

    @staticmethod
    def transform_rating_to_number(label):
        mapping = {"Ex": 5, "Gd": 4, "TA": 3, "Fa": 2, "Po": 1}
        return mapping.get(label, 0)

    @staticmethod
    def transform_to_number_bsmt_exposure(label):
        mapping = {"Gd": 5, "Av": 4, "Mn": 3, "No": 2, "NA": 1}
        return mapping.get(label, 0)

    @staticmethod
    def transform_to_boolean(value_for_ok, feature):
        return 1 if value_for_ok == feature else 0

    @staticmethod
    def transform_to_garage_finish(label):
        mapping = {"Fin": 3, "RFn": 2, "Unf": 1, "NA": 0}
        return mapping.get(label, 0)

    @staticmethod
    def transform_paved_drive(label):
        mapping = {"Y": 2, "P": 1, "N": 0}
        return mapping.get(label, 0)

    @staticmethod
    def transform_sale_type(label):
        mapping = {"New": 2, "WD": 1, "NAN": 0}
        return mapping.get(label, 0)

    @staticmethod
    def transform_sale_condition(label):
        mapping = {"Partial": 3, "Normal": 2, "Abnorml": 1, "NAN": 0}
        return mapping.get(label, 0)

    def transform_data(self, df):
        df["SaleCondition"] = df["SaleCondition"].apply(self.transform_sale_condition)
        df["FireplaceQu"] = df["FireplaceQu"].apply(self.transform_rating_to_number)
        df["KitchenQual"] = df["KitchenQual"].apply(self.transform_rating_to_number)
        df["HeatingQC"] = df["HeatingQC"].apply(self.transform_rating_to_number)
        df["BsmtQual"] = df["BsmtQual"].apply(self.transform_rating_to_number)
        df["BsmtCond"] = df["BsmtCond"].apply(self.transform_rating_to_number)
        df["ExterQual"] = df["ExterQual"].apply(self.transform_rating_to_number)
        df["BsmtExposure"] = df["BsmtExposure"].apply(self.transform_to_number_bsmt_exposure)
        df["GarageFinish"] = df["GarageFinish"].apply(self.transform_to_garage_finish)
        df["Foundation"] = df["Foundation"].apply(partial(self.transform_to_boolean, "PConc"))
        df["CentralAir"] = df["CentralAir"].apply(partial(self.transform_to_boolean, "Y"))
        df["PavedDrive"] = df["PavedDrive"].apply(self.transform_paved_drive)
        df["SaleType"] = df["SaleType"].apply(self.transform_sale_type)

        df["GarageCond"] = df["GarageCond"].apply(self.transform_rating_to_number)
        df["GarageQual"] = df["GarageQual"].apply(self.transform_rating_to_number)
        df["ExterCond"] = df["ExterCond"].apply(self.transform_rating_to_number)

        return df

    @staticmethod
    def transform_numerical_data(df):
        df["TotalIndorArea"] = df["1stFlrSF"] + df["2ndFlrSF"]
        return df

    @staticmethod
    def filter_numerical_data_for_training(df):
        df = df[df.Id != 496]

        df = df[df["LotFrontage"] < 250]
        df = df[df["LotArea"] < 100000]
        df = df[df["TotalBsmtSF"] < 3100]

        df = df[df["GarageArea"] < 1200]
        df = df[df["MasVnrArea"] < 1300]
        df = df[df["EnclosedPorch"] < 500]

        return df

    @staticmethod
    def remove_unused_features(df):
        features_to_delete = ["Street", "Alley", "LotShape", "LandContour", "Utilities", "LotConfig", "LandSlope",
                              "Condition1", "Condition2", "BldgType", "HouseStyle", "RoofStyle", "RoofMatl",
                              "Exterior1st", "Exterior2nd", "MasVnrType", "BsmtFinType1", "BsmtFinType2",
                              "Heating", "Electrical", "PoolQC", "Fence", "MiscFeature", "Functional",
                              "GarageType", "MSZoning", "Neighborhood", "MSSubClass", "BsmtUnfSF", "1stFlrSF",
                              "2ndFlrSF", "LowQualFinSF", "BsmtFullBath", "BsmtHalfBath", "KitchenAbvGr",
                              "3SsnPorch", "ScreenPorch", "PoolArea", "MiscVal", "MoSold", "YrSold",
                              "BsmtFinSF1", "BsmtFinSF2", "HalfBath", "BedroomAbvGr", "WoodDeckSF"]

        df = df.drop(features_to_delete, 1)
        return df
