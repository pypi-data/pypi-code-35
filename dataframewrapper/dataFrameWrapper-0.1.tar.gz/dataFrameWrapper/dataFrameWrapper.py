import pandas as pd
import numpy as np

class DataFrameWrapperClass:
    def __init__(self, dataframe):
        self.df = dataframe
        
    def __tuple_apply(self, objects):
        cols, func = objects
        if isinstance(cols, str):
            cols = list(cols)
        for c in cols:
            self.df_copy[c] = self.df_copy[c].apply(func)
        return self
        
    def convert(self, objects):
        self.df_copy = self.df.copy()
        if isinstance(objects, list):
            for tup in objects:
                self.__tuple_apply(tup)
        return self
    
    def add_new(self, objects):
        self.df_copy = self.df.copy()
        for obj in objects:
            self.df_copy[obj[0]] = self.df_copy.apply(obj[1], axis=1)
        return self
    
    def split_cond(self, conditions, return_all=False):
        self.df_copy = self.df.copy()
        returns = []
        indexes = []
        if isinstance(conditions, list):
            for cond in conditions:
                df_cond = self.df_copy.loc[cond]
                returns.append(DataFrameWrapper(df_cond))
                indexes.extend(df_cond.index.tolist())
            rest = self.df_copy.drop(indexes)
            returns.append(DataFrameWrapper(rest)) if len(rest) > 0 else None
            return returns if return_all==True else returns[0]
        else:
            df_cond = self.df_copy.loc[conditions]
            a, b = DataFrameWrapper(df_cond), DataFrameWrapper(self.df_copy.drop(df_cond.index.tolist()))
            return (a, b) if return_all==True else (a,)

    def _eval(self):
        return self.df_copy
    
    def _get(self):
        return self.df
    
    def _set(self):
        self.df = self.df_copy
        return self