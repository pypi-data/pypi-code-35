def rename_columns(data, **kwargs):
    """
    Function renames chosen DataFrame columns to given names. Edited DataFrame
    needs to contain columns with names 'id_user', 'x', 'y' and 'time'

    :param data: Dataframe
    :param kwargs: Any number of arguments in style:
                oldColumnName = 'newColumnName', where oldColumnName
                is current name of column and newColumnName is name it should
                be renamed to.
                newColumnName should be one of the following: 'x', 'y',
                'z', 'time', 'id_user'
    :return: returns DataFrame with renamed columns; raises ValueError if not
            all required columns were specified
    """

    required_columns = {'id_user', 'x', 'y', 'time'}
    new_data = data.rename(columns=kwargs)
    if required_columns.issubset(set(new_data.columns)):
        return new_data
    else:
        raise ValueError('Missing some of the required columns')
