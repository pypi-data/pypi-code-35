"""
Functions to deal with downloading and writting data to the database
"""

import pandas as pd
from sqlalchemy import create_engine

class Get_sql:
    """
    Class that deals with downloading data
    """
    
    def get_google_tree(connection):
        """
        Function to download the google taxonomy tree from the sixads database
        
        Parameters
        ----------
        
        **connection**: sql_alchemy connection object
        
        Returns
        -------
        
            A pandas dataframe 
        """
        sql_query = "SELECT distinct(full_title), id, parent_id, title as class \
                        FROM sixads.sixads_category"

        tree = pd.read_sql_query(sql_query, connection)
        def f(x):
            if x is None:
                return ""
            else:
                return '>' + x
        tree['full_title'] = [f(x) for x in tree['full_title']]
        return tree

    def get_data(connection, select_part, from_part, where_part = ''):
        """
        Function that construcs a query from the given parts and executes it
        
        Parameters 
        ----------
        
        **select_part**: list
            list of strings identifying the desired columns
            
        **from_part**: string 
            the table name 
            
        **where_part**: string
            additional constaints
            
        Returns    
        -------
        
            A pandas dataframe
        """
        columns = ",".join(select_part)
        
        sql_query = "SELECT {columns} \
                    FROM {from_part} \
                    {where_part}".format(columns = columns, 
                                         from_part = from_part, 
                                         where_part = where_part)
                    
        return pd.read_sql_query(sql_query, connection)

class Write_sql:
    """
    Class that deals with writting data
    """
    
    def write_to_table(specs, table, data, if_exists = 'replace'):
        """
        Writes data to the desired table 
        
        Parameters
        ---------
        
        **specs**: dictionary
            Must contain the keys user, password, host and db
            
        **table**: string
            A string refering to the table which we want to write to
            
        **data**: pandas dataframe
            Data which we want to write to the table
            
        **if_exists**: string
            What to do if the table already exists. Possible string values:
            'replace', 'append', 'fail'    
        
        """
        engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(user=specs['user'],
                               pw=specs['password'],
                               host = specs['host'],
                               db=specs['db']))
        data.to_sql(table, con = engine, 
                            if_exists = if_exists, index = False)    
        