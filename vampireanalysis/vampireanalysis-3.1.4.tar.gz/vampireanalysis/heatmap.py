import os 
from time import sleep
import pandas as pd 
import numpy as np 

import seaborn as sns
import matplotlib.pyplot as plt

xlsxpath = 'C:/Users/kuki/Desktop/Desktop/nat prot/figure raw file/slide5/heatmap_num.xlsx'
xlsx = pd.read_excel(xlsxpath,sheet_name='Sheet1',usecols = "D:M")
# xlsx = xlsx.T
ax = sns.heatmap(xlsx,cmap='inferno',linewidths=0.5,annot=True,xticklabels=False,yticklabels=False,center = np.median(xlsx.values)+25)

# data =[0.5,1,2,4,8,12,25,50,99]

# data = np.reshape(data,(1,9))
# ax = sns.heatmap(data,cmap=sns.light_palette((210, 90, 60), input="husl"),linewidths=0.5,annot=False,xticklabels=False,yticklabels=False)
plt.show()