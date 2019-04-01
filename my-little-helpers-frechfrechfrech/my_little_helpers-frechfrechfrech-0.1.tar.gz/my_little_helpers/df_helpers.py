import pandas as pd
import numpy as np

def create_empty_df(columns, dtypes, index=None):
    df = pd.DataFrame(index=index)
    for c,d in zip(columns, dtypes):
        df[c] = pd.Series(dtype=d)
    return df

def set_column_values_to_lowercase(df, columns_to_lowercase):
    df_lower = df.copy()
    for col in columns_to_lowercase:
        df_lower[col] = df_lower[col].str.lower()
    return df_lower

def compile_files_in_folder_into_df(folder_path, filename_like):
    df_all = pd.DataFrame([])
    filepaths = glob.glob('{}/{}'.format(folder_path,filename_like))
    for filepath in filepaths:
        df = pd.read_csv(filepath)
        df_all = pd.concat([df_all, df])
    return df_all
