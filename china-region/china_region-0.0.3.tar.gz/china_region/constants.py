import pandas as pd

# csv_name = '../resource/region.csv'
import resource

csv_name = 'region.csv'
CITY_DF = pd.read_csv(csv_name, engine='python', encoding='utf-8')


