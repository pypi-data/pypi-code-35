import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from IPython.display import display
from . import database as db

def load_credit_card_transactions(cursor):
    """Load the dataframe using the credit card transaction format."""
    col_order = ['card', 'transaction_date', 'vendor',
                 'price', 'notes', 'statement_date']
    col_types = {'price': float}
    order_by = ['transaction_date']
    card_transactions = db.load_dataframe(cursor, col_order,
                                          col_types, order_by=order_by)
    return card_transactions

class Card:
    """
    A class to store and examine the history of a credit card.

    This class saves an entire credit card's history. That data can then be
    used to examine specific prior statements, analyze trends, and otherwise
    operate on the credit card's transactions. The transaction data must be
    loaded from a dataframe.

    Parameters
    ––––––––––
    name : str
        The name of the card (e.g. 'Discover' or 'Visa').
    transactions : DataFrame
        The set of transactions in which to find transactions for this card.
        Should have been produced from a MySQL database.
    """

    def __init__(self, name, transactions):
        self.name = name
        self.transactions = self._filter_transactions(transactions)
        # Compile information on current and previous statements
        self.statement_dates = self.transactions.statement_date
        curr_stmnt_date = self.statement_dates.max()
        self.current_statement = self._get_statement(curr_stmnt_date)
        prev_stmnt_date = self._get_previous_statement_date(curr_stmnt_date)
        self.previous_statement = self._get_statement(prev_stmnt_date)
        # Gather sums by statement
        self.statement_sums = self._get_statement_sums()
        self.statement_mean = self.statement_sums.price.mean()

    def _filter_transactions(self, all_transactions):
        """Extract only transactions for this card."""
        mask = all_transactions.card.str.contains(self.name, case=False)
        card_transactions = all_transactions[mask]
        return card_transactions

    def _get_statement_sums(self):
        """Calculate the total due on each credit card statement."""
        statement_sums = self.transactions.groupby('statement_date').sum()
        return statement_sums

    def _get_previous_statement_date(self, current_statement_date):
        """Get the date of the previous statement."""
        # Mask the dates to only keep non-current dates
        mask = (self.statement_dates != current_statement_date)
        past_statement_dates = self.statement_dates[mask]
        # Find the most recent non-current date
        previous_statement_date = past_statement_dates.max()
        return previous_statement_date

    def _get_statement(self, date):
        """Display transactions from the statement for the given date."""
        current_statement = self.transactions[self.statement_dates == date]
        return current_statement

    def display_statement(self, time='current'):
        """
        Display the requested statement, along with other useful info.

        Parameters
        ––––––––––
        time : str
            The statement to display. Can be either `current` or `previous`.
        """
        if time == 'current':
            adj = 'this'
            statement = self.current_statement
        elif time == 'previous':
            adj = 'last'
            statement = self.previous_statement
        else:
            raise ValueError("The value of `time` must be either 'current' "
                             "or 'previous.")
        total = statement.price.sum()
        # Print/display the information
        print(f"\n\nTransactions on {adj} month's statement:")
        display(statement)
        print(f"\t\t\t{adj.title()} month's total: ${total:.2f}")

def get_monthly_sums(transactions_df):
    """Calculate the total charged for purchases each month."""
    months = transactions_df.transaction_date.dt.to_period('M')
    monthly_sums = transactions_df.groupby(months).sum()
    return monthly_sums

def get_monthly_statement_sums(transactions_df):
    """Calculate the total due on all statements issued in a month."""
    st_sums = statement_sums(transactions_df)
    mon_st_sums = st_sums.groupby(pd.Grouper(freq='M')).sum()
    return mon_st_sums

def get_food_purchases(transactions_df):
    """Select purchases that pertain to food consumption."""
    food_identifiers = ['breakfast','brunch','lunch','dinner','supper',
                        'dessert','snack','groceries']
    td = transactions_df
    return td[td['notes'].str.contains('|'.join(food_identifiers),case=False)]

def get_grocery_purchases(transactions_df):
    """Select only purchases that contained groceries."""
    td = transactions_df
    return td[td['notes'].str.contains('groceries',case=False)]

def historical_plot(dates,expenditures,ax=None,label=None,ylim=None):
    """Create a plot of expenditures over time."""
    if not ax:
        fig, ax = plt.subplots(figsize=(15,5))
    ax.bar(dates,expenditures,label=label,width=10)
    # Format the plot
    fs = 14
    ax.legend(fontsize=fs)
    if ylim: ax.set_ylim(0,ylim)
    ax.set_xlabel('Date',fontsize=fs)
    ax.set_ylabel('Cost [$]',fontsize=fs)
    ax.tick_params(labelsize=16)
    return ax
