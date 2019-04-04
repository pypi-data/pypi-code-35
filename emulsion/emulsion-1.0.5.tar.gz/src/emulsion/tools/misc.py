"""Collection of various useful functions used in EMULSION framework,
especially regarding introspection.

"""


# EMULSION (Epidemiological Multi-Level Simulation framework)
# ===========================================================
# 
# Contributors and contact:
# -------------------------
# 
#     - Sébastien Picault (sebastien.picault@inra.fr)
#     - Yu-Lin Huang
#     - Vianney Sicard
#     - Sandie Arnoux
#     - Gaël Beaunée
#     - Pauline Ezanno (pauline.ezanno@inra.fr)
# 
#     BIOEPAR, INRA, Oniris, Atlanpole La Chantrerie,
#     Nantes CS 44307 CEDEX, France
# 
# 
# How to cite:
# ------------
# 
#     S. Picault, Y.-L. Huang, V. Sicard, P. Ezanno (2017). "Enhancing
#     Sustainability of Complex Epidemiological Models through a Generic
#     Multilevel Agent-based Approach", in: C. Sierra (ed.), 26th
#     International Joint Conference on Artificial Intelligence (IJCAI),
#     AAAI, p. 374-380. DOI: 10.24963/ijcai.2017/53
# 
# 
# License:
# --------
# 
#    Copyright 2016 INRA and Univ. Lille
# 
#    Inter Deposit Digital Number: IDDN.FR.001.280043.000.R.P.2018.000.10000
# 
#    Agence pour la Protection des Programmes,
#    54 rue de Paradis, 75010 Paris, France
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


from   functools                 import partial
from   importlib                 import import_module
from   typing                    import List, Iterable, Tuple, Union, Any

import yaml

import numpy                     as np

from   sortedcontainers          import SortedSet


AGENTS = 1
"""Constant value for the index where list of agents are stored in
'populations' tuples.

"""

POPULATION = 1
"""Constant value for the index where population amounts are stored in
'populations' tuples.

"""

## TODO split module according to functions usage

def load_class(module=None, class_name: str = None, options: dict = {}):
    """Dynamically load the class with the specified *class_name* from the
    given *module*.

    Args:
        module: a Python module, where the class is expected to be located.
        class_name: the name of the class to load
        options: some options

    Returns:
        A tuple composed of the class (type) and the options.

    Todo:
        - clarify the role of *options*
    """
    mod = import_module(module)
    return getattr(mod, class_name), options

def load_module(module_name: str):
    """Dynamically load the module with the specified *module_name* and
    return it.

    Args:
        module_name: the name of a valid Python module (accessible in the
            ``PYTHONPATH`` environment variable).

    Returns:
        A reference to the Python module.

    """
    return import_module(module_name)

def rates_to_probabilities(total_rate: float, rate_values: List[float],
                           delta_t: float = 1) -> List[float]:
    """Transform the specified list of *rate_values*, interpreted as
    outgoing rates, into probabilities, according to the specified
    time step (*delta_t*) and normalized by *total_rate*.

    For exit rates :math:`\\rho_i` (one of the *rate_values*), the
    probability to stay in current state is given by:

    .. math::
        p_0 = e^{-\\delta t.\\sum_i \\rho_i}

    Thus, each rate :math:`\\rho_i` corresponds to a probability

    .. math::
        p_i = \\frac{\\rho_i}{\\sum_i \\rho_i} (1 - p_0)

    Args:
        total_rate: the total exit rate, used for normalization
            purposes. If *rate_values* represent all possible exit
            rates, *total_rate* is their sum.
        rate_values: the list of rates to transform
        delta_t: the value of the time step (expressed in time units)

    Returns:
        The list of probabilities corresponding to the *rate_values*.

    See Also:
        `emulsion.tools.misc.probabilities_to_rates`_

    """
    # compute the exit probability
    base_proba = 1 - np.exp(- total_rate * delta_t)
    # normalize values proportionnally to the rate
    proba_values = [base_proba * rate / total_rate
                    for rate in rate_values]
    # add the probability to stay in the current state
    proba_values.append(1 - base_proba)
    return proba_values

# This function is useful to modellers for the following purposes:
rates_to_probabilities.__USER_FUNCTION__ = ['Rates / probabilities']


def aggregate_probability(probability: float, delta_t: float) -> float:
    """Transform the specified *probability* value, intended to represent
    a probability for events tested each time unit, into the
    probability for the specified time step (*delta_t*).

    Args:
        probability: the probability value of an event (during 1 time unit)
        delta_t: the value of the time step (expressed in time units)

    Returns:
        The probability of the event during *delta_t* time units.
    """
    return 1 - (1 - probability)**delta_t

# This function is useful to modellers for the following purposes:
aggregate_probability.__USER_FUNCTION__ = ['Rates / probabilities']


def aggregate_probabilities(probability_values: Iterable[float],
                            delta_t: float) -> Iterable[float]:
    """From the specified *probability_values*, intended to represent
    probabilities of events duting one time unit, compute the
    probabilities for the specified time step (*delta_t*).

    Args:
        probability_values: a list of probability values for several events
            (during 1 time unit)
        delta_t: the value of the time step (expressed in time units)

    Returns:
        The probabilities of the same events during *delta_t* time units.
    """
    return probability_values if delta_t == 1\
        else tuple(aggregate_probability(p, delta_t)
                   for p in probability_values)

# This function is useful to modellers for the following purposes:
aggregate_probabilities.__USER_FUNCTION__ = ['Rates / probabilities']


def probabilities_to_rates(probability_values: Iterable[float]) -> List[float]:
    """Transform a list of probabilities into a list of rates. The
    last value is expected to represent the probability of staying in
    the current state.

    Args:
        probability_values: a list of probabilities, the last one representing
            the probability to stay in the current state

    Returns:
        A list of rates corresponding to those probabilities.

    See Also:
        `emulsion.tools.misc.rates_to_probabilities`_
    """
    if probability_values[-1] == 1:
        return [0] * (len(probability_values) - 1)
    sum_of_rates = - np.log(probability_values[-1])
    proba_change = 1 - probability_values[-1]
    values = [v * sum_of_rates / proba_change for v in probability_values]
    return values[:-1]

# This function is useful to modellers for the following purposes:
probabilities_to_rates.__USER_FUNCTION__ = ['Rates / probabilities']


# internal usage (TODO: make private to relevant module)
def rewrite_keys(name, position, change_list):
    prefix = name[:position]
    suffix = name[position+1:]
    return [(prefix + (key,) + suffix, value)
            for key, value in change_list]


def count_population(agents_or_pop: Tuple) -> Union[int, float]:
    """Return the amount of atoms represented in *agents_or_pop*.

    Args:
        agents_or_pop: a tuple: either ('population', qty) or
            ('agents', list of agents).

    Returns:
        The amount corresponding to the population: generally, an int
        value, but deterministic models produce float values.
    """
    return agents_or_pop[POPULATION]\
      if 'population' in agents_or_pop\
      else len(agents_or_pop[AGENTS])


def select_random(origin: Iterable, quantity: int,
                  exclude: SortedSet = SortedSet()) -> List:
    """Return a random selection of *quantity* agents from the *origin*
    group, avoiding those explicitly in the *exclude* set. If the
    *origin* population proves too small, all available agents are
    taken, irrespective to the *quantity*.

    Args:
        origin: the population where agents must be selected
        quantity: the number of agents to select in the population
        exclude: agents which are not available for the selection

    Returns:
        A list of randomly selected agents according to the above constraints.
    """
    content = [unit for unit in origin if unit not in exclude]
    size = len(content)
    np.random.shuffle(content)
    return content[:min(quantity, size)]

# This function is useful to modellers for the following purposes:
select_random.__USER_FUNCTION__ = ['Selecting agents']


def read_from_file(filename: str):
    """Read the specified YAML *filename* and return the corresponding
    Python document.

    Args:
        filename: the name of the YAML file to load

    Returns:
        A Python object built by parsing of the YAML file, i.e. either
        a dict, list, or even str/int/etc... (Most YAML document will
        produce dictionaries.)

    """
    with open(filename, 'r') as fil:
        description = yaml.safe_load(fil)
    return description


def retrieve_value(value_or_function, agent):
    """Return a value either directly given by parameter
    *value_or_function* if it is a true value, or computed from this
    parameter seen as a function, with the specified *agent* as argument.

    Args:
        value_or_function: either a callable (function that applies to
            an agent to retrieve an individual value), or the value itself
        agent: the agent to use as parameter of the callable if necessary

    Returns:
        The expected value (agent-based or not).
    """

    return value_or_function(agent)\
        if callable(value_or_function)\
        else value_or_function


def moving_average(values, window_size, mode='same'):
    """Compute a moving average of the specified *values* with respect to
    the *window_size* on which the average is calculated. The return
    moving average has the same size as the original values. To avoid
    boundary effects, use ``mode='valid'``, which produce a result of
    size ``len(values) - window_size + 1``.

    Args:
        values: array-like, contains the values for moving average computation
        window_size: width of the moving average window
        mode: a parameter for `numpy.convolve`

    Returns:
        A numpy ``nd_array`` containing the values of the moving average.

    """
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(values, window, mode)

# This function is useful to modellers for the following purposes:
moving_average.__USER_FUNCTION__ = ['Computations']



def add_new_property(agent, property_name, getter_function):
    """Add a new property to an agent.

    Actually, the property is added to the class of the agent, as
    Python properties are descriptors. Yet, the dynamic attribution of
    properties must me done through instances rather than classes,
    since agents must add the name of the property to their
    ``_mbr_cache`` attribute.

    Args:
        agent (AbstractAgent): the agent to which the property must be
            added
        property_name: the name of the property
        getter_function: the function upon which the property is built

    """
    setattr(agent.__class__, property_name, property(getter_function))
    agent._mbr_cache.add(property_name)
    # print('Agent {} adding property {} to class {}'.format(agent, property_name, agent.__class__))


def create_population_getter(process_name: str,
                             group_name: Union[str, Tuple]):
    """Build a getter for property of the form ``total_X_Y`` where ``X``
    and ``Y`` are states of two different states machines used in a
    grouping.

    The functions can handle groupings with an arbitrary number of states.

    Parameters
    ----------
    process_name : str
        the name of the process associated with the grouping for which
        the population getter is created
    group_name : str or tuple
        either a string representing the state name (if only one), or
        a tuple of several state names

    Returns
    -------
    callable :
        A function which can be applied to an `AbstractProcessManager`
        agent which returns the population size for the specified
        group.

    """
    if not isinstance(group_name, tuple):
        group_name = (group_name,)
    # print('adding automatic property for', process_name, group_name)
    return lambda self: self.get_group_population(process_name, group_name)

def create_counter_getter(machine_name, state_name):
    return lambda self: self.counters[machine_name][state_name]


def create_state_tester(state_name):
    return lambda self: self.is_in_state(state_name)

def create_duration_getter(machine_name):
    # print('adding automatic property for', process_name, group_name)
    return lambda self: self.duration_in_current_state(machine_name)

def add_all_test_properties(agent):
    for machine in agent.model.state_machines.values():
        add_new_property(agent, 'duration_in_{}'.format(machine.machine_name),
                         create_duration_getter(machine.machine_name))
        for state in machine.states:
            add_new_property(agent, 'is_{}'.format(state.name),
                             create_state_tester(state.name))


def find_operator(operator: str):
    """Return an aggregation function named *operator*.

    Search starts with emulsion functions (module
    `emulsion.tools.functions`), which includes Python built-ins, then
    in `numpy`.

    A special shortcut is provided for percentiles: ``percentileXX``
    is interpreted as the partial function
    ``numpy.percentile(q=int(XX))``.

    Args:
        operator: the name of the aggregation operator

    Returns:
        A function that takes a list (or array-like) as input and
        returns the application of the *operator* to the values.

    """
    op = None
    current_module = import_module('emulsion.tools.functions')
    # search in emulsion functions module first
    if hasattr(current_module, operator):
        op = getattr(current_module, operator)
    elif operator.startswith('percentile'):
        # special case of 'percentileXX' where XX is a number (0 to
        # 100) and automatically extracted
        op = partial(np.percentile, q=int(operator[10:]))
    else:
        # otherwise search in numpy
        op = getattr(np, operator)
    return op

def create_aggregator(sourcevar: str, operator: str):
    """Create an aggregator function to be used as property getter. This
    aggregator function has to collect all values of *sourcevar* for
    agents contained in a given host, and reduce them to one avalue
    using the specified *operator*.

    Args:
        sourcevar: the name of the variable to collect in the sublevel
        operator: the name of the operator to apply to the collected values

    Returns:
        A function which can be applied to a `MultiProcessManager`
        agent (i.e. with explicit sublevel agents) which returns the
        aggregated values for the whole population.

    """
    op = find_operator(operator)
    return lambda self: op([sublevel.get_information(sourcevar)
                            for sublevel in self['MASTER']])

def create_group_aggregator(sourcevar: str, operator: str, process_name: str,
                            group_name: Union[str, Tuple]):
    """Build a getter for property of the form ``newvar_X_Y`` where ``X``
    and ``Y`` are states of two different states machines used in a
    grouping, ``newvar`` is an aggregate variable based on collecting
    all values of *sourcevar* for the specific *group_name* and
    aggregating the values using *operator*. The functions can handle
    groupings with an arbitrary number of states.

    Args:
        sourcevar: the name of the variable to collect in the sublevel
        operator: the name of the operator to apply to the collected values
        process_name: the name of the process associated with the
          grouping for which the population getter is created
        group_name: either a string representing the state name (if
          only one), or a tuple of several state names

    Returns:
        A function which can be applied to an `MultiProcessManager`
        agent (i.e. with explicit sublevel agents) which returns the
        aggregated value for the specified group.

    """
    op = find_operator(operator)
    if not isinstance(group_name, tuple):
        group_name = (group_name,)
    # print('adding automatic property for', process_name, group_name)
    def aggregate_group(self):
        try:
            return op([sublevel.get_information(sourcevar)
                       for sublevel in self.get_group_atoms(process_name, group_name)])
        except ValueError:
            return np.nan
    return aggregate_group

def create_atoms_aggregator(sourcevar: str, operator: str,
                            machine_name: str, state_name: str):
    """Build a getter for property of the form ``newvar_X`` where ``X`` if
    the value of *state_name* (a state of *state_machine*), ``newvar``
    is an aggregate variable based on collecting all values of
    *sourcevar* for the specific *group_name* and aggregating the
    values using *operator*. This function is intended to work on
    `IBMProcessManager` agents, which do not benefit from groupings.

    Args:
        sourcevar: the name of the variable to collect in the sublevel
        operator: the name of the operator to apply to the collected values
        machine_name: the name of the state machine for which the
          getter is created
        state_name: the state name

    Returns:
        A function which can be applied to an `IBMProcessManager`
        agent (i.e. with explicit but ungrouped sublevel agents) which
        returns the aggregated value for the specified group.

    """
    op = find_operator(operator)
    def aggregate_atoms(self):
        try:
            return op([sublevel.get_information(sourcevar)
                            for sublevel in self.select_atoms(machine_name, state=state_name)])
        except ValueError:
            return np.nan
    return aggregate_atoms

def serial(start=0, end=None, model=None):
    """A very simple serial number generator."""
    value = start
    while True:
        yield value
        value += 1
        if end is not None:
            if value >= model.get_value(end):
                value = start


def create_new_serial(end=None, model=None):
    """Create the serial number generator associated to the specified
    variable.

    """
    generator = serial(start=0, end=end, model=model)
    return lambda self: next(generator)
