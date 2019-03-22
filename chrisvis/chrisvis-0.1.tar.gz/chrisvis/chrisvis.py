import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def chrisfreqplot(series, x=10):
    ''' A funciton to take a series of data and output the top occurring categories

    INPUTS - a data series, optionally a number of categories to show (default 10)
    OUTPUTS - a bar plot
    '''
    names, count = np.unique(series, return_counts=True)
    #Find the unique values and the count of them
    df = pd.DataFrame(
        data = {'label': names, 'value': count},
        ).sort_values('value', ascending = False)
    #Take the first X values
    df2 = df[:x].copy()

    #Calculate how many fall into the 'other' Category
    new_row = pd.DataFrame(data = {
        'label' : ['others'],
        'value' : [df['value'][x:].sum()]
    })

    #combining top x with others
    df2 = pd.concat([df2, new_row])
    #create the graph
    y_pos = np.arange(len(df.value))
    ax = sns.barplot(x='label', y='value', data = df2)
    for item in ax.get_xticklabels():
        item.set_rotation(90)
    ax.set(xlabel='', ylabel='Count')
