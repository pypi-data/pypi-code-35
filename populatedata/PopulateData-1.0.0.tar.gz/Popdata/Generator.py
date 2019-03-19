import random

import pandas as pd


class Generator:

    def __init__(self, mode='Random', size = None, col_dict = None):
        self.mode = mode
        self.size = size
        self.col_dict = col_dict

    def generate_new_values(self, col_dict):
        new_values = []
        for k, v in col_dict.items():
            if v[-1] == 'int64':
                new_values.append(random.randint(v[0], v[1]))
            elif v[-1] == 'float64':
                new_values.append(random.randrange(v[0], v[1]))
            else:
                new_values.append(random.choice(v))
        return new_values

    def change_type(self, df, col_dict):
        for col in df.columns:
            if col_dict[col][-1] == 'int64':
                df[col] = df[col].astype('int64')
            elif col_dict[col][-1] == 'float64':
                df[col] = df[col].astype('float64')
            else:
                pass
        return df

    def generate(self, row_num, col_dict):
        df = pd.DataFrame(columns=col_dict.keys())
        print (df.dtypes)
        # print ([random.choice(col_dict[k]) for k in col_dict.keys()])
        generate_size = self.size - row_num
        if generate_size > 0:
            if self.mode == 'Random':
                for _ in range(generate_size):
                    new_values = self.generate_new_values(col_dict)
                    new_df = pd.DataFrame([new_values], columns=col_dict.keys())

                    df = df.append(new_df, ignore_index=True)
                print (df.dtypes)
        return df
gen = Generator(size = 100)
df = gen.generate(row_num=90, col_dict={'Age': [19, 75, 'int64'], 'Sex': ['male', 'female'], 'Job': [0, 3, 'int64'], 'Housing': ['own', 'free', 'rent'], 'Saving accounts': ['little', 'quite rich', 'rich', 'moderate'], 'Checking account': ['little', 'moderate', 'rich'], 'Credit amount': [250, 18424, 'int64'], 'Duration': [4, 72, 'int64'], 'Purpose': ['radio/TV', 'education', 'furniture/equipment', 'car', 'business', 'domestic appliances', 'repairs', 'vacation/others'], 'Risk': ['good', 'bad']})
#)
# print (gen.generate_new_values(col_dict={'Age': [19, 75, 'int64'], 'Sex': ['male', 'female'], 'Job': [0, 3, 'int64'], 'Housing': ['own', 'free', 'rent'], 'Saving accounts': ['little', 'quite rich', 'rich', 'moderate'], 'Checking account': ['little', 'moderate', 'rich'], 'Credit amount': [250, 18424, 'int64'], 'Duration': [4, 72, 'int64'], 'Purpose': ['radio/TV', 'education', 'furniture/equipment', 'car', 'business', 'domestic appliances', 'repairs', 'vacation/others'], 'Risk': ['good', 'bad']}
# ))
df2 = gen.change_type(col_dict={'Age': [19, 75, 'int64'], 'Sex': ['male', 'female'], 'Job': [0, 3, 'int64'], 'Housing': ['own', 'free', 'rent'], 'Saving accounts': ['little', 'quite rich', 'rich', 'moderate'], 'Checking account': ['little', 'moderate', 'rich'], 'Credit amount': [250, 18424, 'int64'], 'Duration': [4, 72, 'int64'], 'Purpose': ['radio/TV', 'education', 'furniture/equipment', 'car', 'business', 'domestic appliances', 'repairs', 'vacation/others'], 'Risk': ['good', 'bad']}, df=df)
print (df2)
print (df2.dtypes)