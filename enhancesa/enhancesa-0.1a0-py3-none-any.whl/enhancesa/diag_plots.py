# TODO: Improve plot aesthethics, e.g. add hlines
# TODO: Add Cooke's distance and lines 

# Dependencies
import matplotlib.pyplot as plt
import seaborn as sns 
import statsmodels.api as sm
import numpy as np



def diag_plots(model, y):
    """ Produce the four R-style OLS diagnostics plots.  

    Parameters
    ----------
    model : Statsmodels.api.ols object
        A fitted Statsmodels ols model.  
    y : numpy array, pandas series/dataframe
        The response/target variable of the model.

    Returns
    -------
    matplotlib.pyplot figure
        A 2-by-2 figure containing four diagnostics plots.
     
    Examples
    --------
    >>> # Generate data with numpy
    >>> x = np.random.uniform(size=100)
    >>> y = 2 + 0.5*x + np.random.normal(size=100)
    >>> # Put into a pandas df because of Statsmodels requirement
    >>> df = pd.DataFrame(data={'x':x, 'y', y})
    >>> # Create the ols model from statsmodels.formula.api
    >>> model = ols('y ~ x', data=df).fit()
    >>> # Create the plots
    >>> enhancesa.diag_plots(model, y)
    """

    _, axes = plt.subplots(figsize=(15, 8), nrows=2, ncols=2)
    ax1, ax2, ax3, ax4 = axes.flatten()

    # Fitted vs. residuals plot
    sns.residplot(model.fittedvalues, model.resid, 
                    lowess=True, line_kws={'color':'red'}, ax=ax1)
    ax1.set_xlabel('Fitted Values')
    ax1.set_ylabel('Residuals')

    # Quantiles-Quantiles plot
    sm.qqplot(y, line='r', ax=ax2)

    # Standardized residuals vs. fitted values plot
    sns.regplot(model.fittedvalues, np.array(np.sqrt(abs(model.resid))), 
                    lowess=True, line_kws={'color':'red'}, ax=ax3)
    ax3.set_xlabel('Fitted Values')
    ax3.set_ylabel(r'$\sqrt{|Standardized \ Residuals|}$')

    # Leverage vs. standardized residuals plot
    standard_resid = model.get_influence().summary_frame()['standard_resid']
    leverage = model.get_influence().hat_matrix_diag
    sns.regplot(leverage, standard_resid, 
                        lowess=True, line_kws={'color':'red'}, ax=ax4)
    ax4.set_xlim(0, max(leverage)+0.005)
    ax4.set_xlabel('Leverage')
    ax4.set_ylabel('Standardized Residuals')

    # Set horizontal spacing between plot and show
    plt.subplots_adjust(hspace=0.3)
    plt.show()