import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as plt
import seaborn as sns

def plot_3d_with_hue(df, cols = ['x','y','z'], hue_col='hue', title='', \
    xlabel='X', ylabel='Y', zlabel='Z', figsize=(8,8), hue_color_dict={}\
    fig_filepath=None):
    '''
    Generalized function to plot pandas dataframe values in 3d
    df: DataFrame containing the datapoints to plot and a column which corresponds to hue
    cols: list of column names. default=['x','y','z']
    title, xlabel, ylabel, figsize: args for plot
    hue_col: Variables that define subsets of the data, which will be drawn on separate facets in the grid
    hue_color_dict: optional, dictionary of colors which correspond to each hue value. keys are values in hue_col, values are colors
    '''
    fig = plt.figure(figsize=figsize)
    ax = Axes3D(fig)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)

    for val in df[hue_col].unique():
        df_val = df[df[hue_col]==val].copy()
        if val in hue_color_dict.keys():
            ax.scatter(df_val[cols[0]], df_val[cols[1]], df_val[cols[2]], label=val, color=hue_color_dict[val])
        else:
            ax.scatter(df_val[cols[0]], df_val[cols[1]], df_val[cols[2]], label=val)

    plt.legend()

    if fig_filepath!=None:
        plt.savefig(fig_filepath)

    plt.show();

def plot_correlation_heatmap(data, title='', xlabel='X', ylabel='Y', \
        figsize=(8,8), fig_filepath=None):
    '''
    Generalized function to plot correlation between pandas dataframe columns
    data: dataframe with columns to calculate correlation
    title, xlabel, ylabel, figsize: args for plot
    fig_filepath: optional, filepath to save fig
    '''
    sns.set(style="white")
    corr=data.corr()
    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    fig, ax = plt.subplots(figsize=figsize)
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    ax.set_title('Correlation Heatmap of Variables', fontdict={'fontsize':18})
    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if fig_filepath!=None:
        plt.savefig(fig_filepath)
    plt.show()
