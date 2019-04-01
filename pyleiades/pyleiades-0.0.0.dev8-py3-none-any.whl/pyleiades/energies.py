import pandas as pd
from .utils.load_data import load_dataset
from .utils.eia_codes import name_to_code, date_to_code


class Energy:
    """
    Collect energy data for a user-defined energy source.

    Retrieves data from the specified energy source according to specific
    attributes, such as energy consumed per decade, per year, or all years in
    which more than a certain amount of energy was consumed from that source.
    Use this class to extract and return pure data from the dataset.

    Attributes
    ––––––––––
    energy_type : str
        The type of energy source.
    stat_type : str
        The type of statistic ('production', 'consumption', 'import' or
        'export').
    energy_data : DataFrame
        The complete set of energy data from the EIA MER.
    monthly_data : DataFrame
        All monthly data values from the EIA MER.
    yearly_data : DataFrame
        All yearly data values from the EIA MER.

    Parameters
    ––––––––––
    energy_type : str
        The type of energy source to be pulled from the dataset.
    data : DataFrame, optional
        The EIA dataset to be used. Must be three columns: date, energy
        quantity, and energy code. If omitted, use the default dataset.
    stat_type : str
        The type of statistic to be collected ('production', 'consumption',
        'import', or 'export').
    data_date: str
        The date identifier of the dataset. (The default value is `None`, which
        automatically uses the most recently downloaded dataset.)
    """

    def __init__(self, energy_type, data=None,
                 stat_type='consumption', data_date=None):
        self.energy_type = energy_type
        self.stat_type = stat_type
        # Determine energy code from energy source name
        energy_code = name_to_code(energy_type)

        # Use default dataset if dataset argument is omitted
        if data is None:
            data = load_dataset(dataset_date=data_date, dataset_type=stat_type)

        # Isolate this energy's data, separate frequencies, and format the data
        self.energy_data = self._isolate_energy(energy_code, data)
        self.monthly_data, self.yearly_data = self._sep_freqs(self.energy_data)

        self._freq_errmsg = ('Frequency "{}" is not compatible with this data; '
                             'see documentation for permissible frequencies.')
        self._extr_errmsg = ('Input "{}" is not recognized as an extrema; '
                             'try "max" or "min"')

    def _isolate_energy(self, energy_code, data):
        """
        Isolate one type of energy in the given dataset.

        Parameters
        ––––––––––
        energy_code : int
            The energy code corresponding to the energy source to be selected.
        data : DataFrame
            The dataset containing all energy values across energy sources.

        Returns
        –––––––
        energy_data : DataFrame
            A trimmed version of the original dataset, now with only the
            selected energy source. The energy code column is removed.
        """
        energy_data = data[data.energy_code == energy_code]
        return energy_data[['date_code', 'value']]

    @staticmethod
    def _sep_freqs(data):
        """
        Separate the data into monthly and yearly intervals.

        Parameters
        ––––––––––
        data : DataFrame
            The dataset to be partitioned into monthly and yearly intervals.

        Returns
        –––––––
        monthly_data : DataFrame
            A subset of the data with the energy values reported monthly.
        yearly_data : DataFrame
            A subset of the data with the energy values reported yearly.
        """
        # Separate monthly and yearly totals
        monthly_data = data[data.date_code.str[-2:] != '13'].copy()
        yearly_data = data[data.date_code.str[-2:] == '13'].copy()
        # Index the dataframes by the date
        for df in monthly_data, yearly_data:
            df.rename(index=str, columns={'date_code': 'date'}, inplace=True)
            df.set_index('date', inplace=True);
        # Remove date code '13' from end of yearly dates
        yearly_data.index = yearly_data.index.str.slice(stop=4)
        return monthly_data, yearly_data

    @staticmethod
    def _daterange(data, start_date, end_date):
        """
        Resize the dataset to cover only the date range specified.

        Parameters
        ––––––––––
        data : DataFrame
            A dataframe containing the data to be resized. The index must be
            in the format of the EIA date code ('YYYYMM').
        start_date, end_date : str
            The dataset start/end dates (both inclusive) as strings ('YYYYMM').

        Returns
        –––––––
        bound_data : DataFrame
            A dataframe corresponding to the specified date range.
        """
        # Use dataset default dates unless otherwise specified by the user
        if start_date is None:
            start_date = data.index.min()
        else:
            start_date = date_to_code(start_date)
            start_date = start_date[:len(data.index[0])]
        if end_date is None:
            end_date = data.index.max()
        else:
            end_date = date_to_code(end_date)
            end_date = end_date[:len(data.index[0])]

        # Adjust dataset boundaries 
        half_bounded_data = data[data.index >= start_date]
        bounded_data = half_bounded_data[half_bounded_data.index <= end_date]
        return bounded_data

    def totals(self, freq='yearly', start_date=None, end_date=None, ):
        """
        Get the energy statistic totals over a given period.

        This method aggregates energy statistic totals according to a user
        defined frequency—either monthly, yearly, or cumulatively. Data is
        collected for the entire dataset unless specific dates are given.
        When dates are provided, the totals are only returned on that time
        interval, with inclusive starting and ending dates. If data at the
        specified frequency does not exist for the entire interval, the interval
        will be automatically adjusted to fit the available data in the
        interval. Cumulative totals use yearly data, and so only include data up
        until the last complete year.

        Parameters
        ––––––––––
        freq : str
            The frequency for gathering totals ('monthly','yearly',or
            'cumulative').
        start_date, end_date : str
            The user specified starting and ending dates for the dataset
            (both inclusive); for 'monthly', acceptable formats are 'YYYYMM',
            'YYYY-MM', or 'MM-YYYY' (dashes can be substituted for periods,
            underscores, or forward slashes); for 'yearly' or 'cumulative',
            give only the full year, 'YYYY'.

        Returns
        –––––––
        totals_data : DataFrame, float
            A dataframe containing totals in the specified interval at the
            given frequency, a floating point number if a cumulative sum.
        """
        # Bound data at requested frequency by start and end dates
        if freq == 'monthly':
            full_data = self.monthly_data
        elif freq == 'yearly' or freq == 'cumulative':
            full_data = self.yearly_data
        else:
            raise ValueError(self._freq_errmsg.format(freq))
        totals_data = self._daterange(full_data, start_date, end_date)
        # For cumulative totals, take the sum
        if freq == 'cumulative':
            totals_data = totals_data.value.sum()
        return totals_data

    def maxima(self, freq='yearly', start_date=None, end_date=None):
        """
        Get the maximum energy consumed over a given period (see extrema).
        """
        self.extrema('max', freq=freq, start_date=start_date,
                     end_date=end_date)

    def minima(self, freq='yearly', start_date=None, end_date=None):
        """
        Get the minimum energy consumed over a given period (see extrema).
        """
        self.extrema('min', freq=freq, start_date=start_date,
                     end_date=end_date)

    def extrema(self, extremum, freq='yearly', start_date=None, end_date=None):
        """
        Get the maximum/minimum energy consumed over a given period.

        Parameters
        ––––––––––
        extremum : str
            The exteme value to be found ('max' or 'min').
        freq : str
            The frequency for checking extrema ('monthly' or 'yearly').
        start_date, end_date : str
            The user specified starting and ending dates for the dataset
            (both inclusive); for 'monthly', acceptable formats are 'YYYYMM',
            'YYYY-MM', or 'MM-YYYY' (dashes can be substituted for periods,
            underscores, or forward slashes); for 'yearly' or 'cumulative',
            give only the full year, 'YYYY'.

        Returns
        –––––––
        extrema_date : string
            A string representation of the month in which the extreme value
            occurred (format 'YYYY' or 'YYYYMM')
        extreme_value : float
            A dataframe giving the specified extreme value and the date of
            occurrence for that value.
        """
        # Bound data by start and end dates
        if freq == 'monthly':
            full_data = self.monthly_data
        elif freq == 'yearly':
            full_data = self.yearly_data
        else:
            raise ValueError(self._freq_errmsg.format(freq))
        extremum_data = self._daterange(full_data, start_date, end_date)

        # Select max or min
        extremum = extremum.lower()[:3]
        if extremum == 'max':
            extremum_val = extremum_data.value.max()
        elif extremum == 'min':
            extremum_val = extremum_data.value.min()
        else:
            raise ValueError(self._extr_errmsg.format(extremum))
        extremum_data = extremum_data[extremum_data.value == extremum_val]
        extremum_date = extremum_data.index[0]
        extreme_value = extremum_data.value[0]
        return extremum_date, extreme_value

    def more_than(self, amount, start_date, end_date, interval):
        """
        Get data for intervals with more energy consumption than a given level.

        Parameters
        ––––––––––
        amount: float
            The lower boundary (exclusive) for which data may be included in
            the dataset.
        start_date, end_date : str
            The user specified dataset starting and ending dates (both
            inclusive); acceptable formats are 'YYYYMM', 'YYYY-MM', or
            'MM-YYYY'. Dashes ("-") can be substituted for periods ("."),
            underscores ("_"), or forward slashes ("/").
        interval : str
            The time intervals considered for extrema comparison ('yearly',or
            'monthly').
        """
        raise NotImplementedError



    """
    Additonal potential options to add:
        - average yearly energy consumed
        - average seasonal energy consumed
        - consolidate date range selection and monthly/yearly/cumulative selection into a _formatdata method
    """

