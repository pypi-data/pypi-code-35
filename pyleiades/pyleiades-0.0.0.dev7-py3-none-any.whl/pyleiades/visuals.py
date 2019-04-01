import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from pyleiades.energies import Energy


class Visual:
    """
    Create visuals based on energy data.

    Takes one or more energy histories as input upon initialization, providing
    methods to visualize the data (including the ability to make comparisons
    across energy sources if more than one energy is given. Visualizations
    include histograms, line graphs, pie charts, and animations.

    Attributes
    ––––––––––
    data : DataFrame, optional
        The EIA dataset on which visualizations are based.
    stat_type : str
        The type of statistic ('production', 'consumption', 'import' or
        'export').
    data_date : str
        The date identifier of the dataset. (The default value is `None`, which
        automatically uses the most recently downloaded dataset.)
    energies : list of Energy object
        A list of energies from the dataset to be visualized.

    Parameters
    ––––––––––
    energy_types : str or list of str, optional
        A list of one or more energies to be displayed.
    data : DataFrame, optional
        The EIA dataset to be used. Must be three columns: date, energy
        quantity, and energy code. If omitted, use the default dataset.
    stat_type : str
        The type of statistic to be displayed ('production', 'consumption',
        'import', or 'export').
    data_date : str
        The date identifier of the dataset. (The default value is `None`, which
        automatically uses the most recently downloaded dataset.)
    """

    def __init__(self, energy_types=None, data=None, stat_type='consumption',
                 data_date=None):
        self.data = data
        self.stat_type = stat_type
        self.data_date = data_date
        self.energies = []
        if energy_types is not None:
            if type(energy_types) is str:
                self.include_energy(energy_types)
            elif type(energy_types) is list:
                self.include_energy(*energy_types)
            else:
                raise ValueError("The input energy type(s) must be a single "
                                 "string or a list.")

        self._empty_errmsg = ('No energy histories have been chosen yet for '
                             'the visual.')
        self._subj_errmsg = ('Subject "{}" is not compatible with this visual; '
                           'see documentation for permissible subjects.')

    def include_energy(self, *energy_types):
        """
        Include energy source(s) in the visual.

        Parameters
        ––––––––––
        energy_types : str
            The type(s) of energy source to be pulled from the dataset.
        """
        for energy_type in energy_types:
            energy = Energy(energy_type, data=self.data,
                            stat_type=self.stat_type, data_date=self.data_date)
            self.energies.append(energy)

    def linegraph(self, subject, freq='yearly', start_date=None, end_date=None):
        """
        Make a line graph of the chosen energy source histories.

        Parameters
        ––––––––––
        subject : str
            The subject of the line graph ('totals','maxima', or 'minima').
        freq : str
            The frequency for checking extrema ('monthly' or 'yearly').
        start_date, end_date : str
            The user specified starting and ending dates for the dataset
            (both inclusive); for 'monthly', acceptable formats are 'YYYYMM',
            'YYYY-MM', or 'MM-YYYY' (dashes can be substituted for periods,
            underscores, or forward slashes); for 'yearly' or 'cumulative',
            give only the full year, 'YYYY'.
        """
        if len(self.energies) == 0:
            raise RuntimeError(self._empty_errmsg)

        # Get data for the selected subject and merge into one dataframe
        if subject == 'totals':
            subject_data = [energy.totals(freq, start_date, end_date)
                            for energy in self.energies]
        elif subject == 'maxima':
            subject_data = [energy.extrema('max', freq, start_date, end_date)
                            for energy in self.energies]
        elif subject == 'minima':
            subject_data = [energy.extrema('min', freq, start_date, end_date)
                            for energy in self.energies]
        else:
            raise ValueError(self._subj_errmsg.format(subject))
        graph_data = pd.concat(subject_data, axis=1)
        graph_data.columns = [energy.energy_type for energy in self.energies]
        dates = graph_data.index

        # Generate the plot
        fig, ax = plt.subplots(figsize=(10,6))
        for column in graph_data.columns:
            data_points = len(graph_data)
            ax.plot(range(data_points), graph_data[column], label=column)
        ax.set_title(f'Energy {self.stat_type} history')
        if freq == 'yearly':
            interval = 10
            xticklabels = dates[::interval]
        elif freq == 'monthly':
            interval = 120
            xticklabels = [f'{_[-2:]}/{_[:-2]}' for _ in dates[::interval]]
        ax.set_xlim(0, data_points)
        ax.set_xticks(range(0, data_points, interval))
        ax.set_xticklabels(xticklabels)
        ax.set_ylabel('Energy [QBTU]')
        ax.legend()
        return ax
