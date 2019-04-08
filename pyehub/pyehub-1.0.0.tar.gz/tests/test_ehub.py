import pytest
import os
from energy_hub import EHubModel

"""
Tests for the EHubModel 

To run all the tests:
    $ pytest 
    
"""


def calc_results(excel_file):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    excel = os.path.join(current_directory, excel_file)

    model = EHubModel(excel=excel)

    results = model.solve(is_verbose=False)
    return results


def the_model(excel_file):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    excel = os.path.join(current_directory, excel_file)

    model = EHubModel(excel=excel)
    return model


def test_storage_of_same_type_both_used():
    """Ensure that multiple storages that hold the same stream are all
    used."""
    results = calc_results('storages_of_same_type.xlsx')
    variables = results['solution']

    assert variables['Grid'] == 0

    for t in [1, 2]:
        assert variables['energy_input'][t]['PV'] == 50

    for t in [2, 4]:
        assert variables['storage_level'][t]['RightBattery'] == 50

    assert variables['storage_level'][3]['LeftBattery'] == 50

    assert variables['energy_from_storage'][4]['RightBattery'] == 50
    assert variables['energy_from_storage'][3]['LeftBattery'] == 50

    assert variables['storage_level'][5]['LeftBattery'] == 0
    assert variables['storage_level'][5]['RightBattery'] == 0

    assert variables['total_carbon'] == 0
    assert variables['total_cost'] == 17832.5


def test_storage_levels_loop():
    """Ensure that the storage level can transfer levels from the end to
    beginning."""

    excel_files = ['storage_looping.xlsx', 'storage_level_.xlsx', 'storages_of_same_type.xlsx',
                  'test_file.xlsx']

    for excel in excel_files:
        results = calc_results(excel)
        variables = results['solution']

        storage_level = variables['storage_level']
        storages = variables['storages']
        t = len(variables['time'])

        for storage in storages:
            assert storage_level[0][storage] == storage_level[t][storage], f"\n " \
            f"Failed for the following excel file: {excel}"


def test_no_exporting_from_storage_on_first_time_step_with_no_demands():
    """Ensures that no energy is taken from a storage and immediately
    exported on the first time step when there is no energy in the
    storage."""
    results = calc_results('storage_export_start.xlsx')
    variables = results['solution']
    parameters = results['solution']

    for t in range(0, 3):
        assert parameters['LOADS']['Elec'][t] == 0
        assert variables['energy_from_storage'][t]['Battery'] == 0

    assert variables['total_carbon'] == 0
    assert variables['total_cost'] == 0


def test_simple_chp():
    """Ensure a simple CHP converter works."""
    results = calc_results('chp.xlsx')
    variables = results['solution']

    assert variables['Grid'] == 0  # Don't use any Grid

    energy_input = variables['energy_input']
    for t in range(0, 4):
        assert energy_input[t]['CHP'] == 50

    assert variables['total_cost'] == 784.25


def test_multiple_demand_streams():
    """Ensure that we can have multiple demand streams."""
    results = calc_results('elec_and_heat_demands.xlsx')
    variables = results['solution']

    energy_imported = variables['energy_imported']
    energy_input = variables['energy_input']
    for t in range(0, 4):
        assert energy_input[t]['PV'] == 50
        assert energy_input[t]['Boiler'] == 50
        assert energy_imported[t]['Grid'] == 0

    assert variables['total_cost'] == 1039


def test_ensure_pv_works():
    """Ensure that PV works."""
    results = calc_results('pv.xlsx')
    variables = results['solution']

    energy_imported = variables['energy_imported']
    energy_input = variables['energy_input']
    for t in [0, 3]:
        assert energy_input[t]['PV'] == 50
    assert energy_input[1]['PV'] == 15
    assert energy_input[2]['PV'] == 25
    assert energy_input[1]['Grid'] == 35
    assert energy_input[2]['Grid'] == 25

    assert energy_imported[1]['Grid'] == 35
    assert energy_imported[2]['Grid'] == 25
    for t in [0, 3]:
        assert energy_input[t]['Grid'] == 0

    assert variables['total_cost'] == 17846.9


def test_ensure_fixed_capital_costs_are_added():
    """Ensure there are fixed capital costs."""
    results = calc_results('fixed_capital_costs.xlsx')
    parameters = results['solution']

    assert parameters['FIXED_CAPITAL_COSTS']['Grid'] == 0
    assert parameters['FIXED_CAPITAL_COSTS']['PV'] == 100


def test_storage_works():
    """Ensure that storages work."""
    results = calc_results('storage.xlsx')
    variables = results['solution']

    storage_level = variables['storage_level']
    battery = 'Battery'

    storage_levels = [0, 0, 50, 100, 50, 0]
    for t, level in enumerate(storage_levels):
        assert storage_level[t][battery] == level

    assert variables['total_cost'] == 17832.5


def test_streams_imported():
    """ Ensure that the imported streams are imported  """

    file = 'imported_streams.xlsx'
    results = calc_results(file)
    variables = results['solution']
    model = the_model(file)

    assert model._data.import_streams == ['Grid', 'Gas']

    assert variables['import_streams'] == ['Grid', 'Gas']

    energy_imported = variables['energy_imported']
    for t in range(0, 4):
        assert energy_imported[t]['Gas'] == 50
        assert energy_imported[t]['Grid'] == 0


def test_streams_exported():
    """ Ensure that the exported stream is exported (PV_Elec) """

    file = 'exported_streams.xlsx'
    results = calc_results(file)
    variables = results['solution']
    model = the_model(file)

    assert model._data.export_streams == ['PV_Elec']

    energy_exported = variables['energy_exported']
    assert variables['export_streams'] == ['PV_Elec']
    for t in range(0, 4):
        assert energy_exported[t]['PV_Elec'] == 50

    assert variables['total_carbon'] == 7.4


def test_investment_cost():
    """Ensure investment cost calculated correctly"""

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    net_present_value_storage = variables['NET_PRESENT_VALUE_STORAGE']
    linear_storage_costs = variables['LINEAR_STORAGE_COSTS']
    storages = variables['storages']
    technologies = variables['technologies']
    net_present_value_tech = variables['NET_PRESENT_VALUE_TECH']
    linear_capital_costs = variables['LINEAR_CAPITAL_COSTS']
    fixed_capital_costs = variables['FIXED_CAPITAL_COSTS']
    is_installed = variables['is_installed']

    storage_cost = sum(net_present_value_storage[storage]
                       * linear_storage_costs[storage]
                       * variables[storage]
                       for storage in storages)

    tech_cost = sum(net_present_value_tech[tech]
                    * (linear_capital_costs[tech]
                       * variables[tech]
                       + fixed_capital_costs[tech]
                       * is_installed[tech])
                    for tech in technologies)

    investment_cost = variables['investment_cost']
    calculated_investment_cost = tech_cost + storage_cost
    calculated_investment_cost = round(calculated_investment_cost, 2)

    assert investment_cost == calculated_investment_cost


def test_operating_cost():
    """Ensure operating cost is correct"""

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    operating_cost = variables['operating_cost']

    export_streams = variables['export_streams']
    import_streams = variables['import_streams']
    energy_exported = variables['energy_exported']
    energy_imported = variables['energy_imported']
    feed_in_tariffs = variables['FEED_IN_TARIFFS']
    fuel_prices = variables['FUEL_PRICES']
    time = len(variables['time'])

    total_export_income = 0
    for stream in export_streams:
        total_energy_exported = sum(energy_exported[t][stream]
                                    for t in range(0, time))
        price = feed_in_tariffs[stream]
        total_export_income += price * total_energy_exported

    total_fuel_bill = 0
    for stream in import_streams:
        total_energy_used = sum(energy_imported[t][stream]
                                for t in range(0, time))
        price = fuel_prices[stream]
        total_fuel_bill += price * total_energy_used

    calculated_operating_cost = total_fuel_bill - total_export_income

    operating_cost = round(operating_cost, 3)
    calculated_operating_cost = round(calculated_operating_cost, 3)

    assert operating_cost == calculated_operating_cost


def test_maintenance_cost():
    """Ensure maintenance cost is correct"""

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    maintenance_cost = variables['maintenance_cost']

    time = len(variables['time'])
    technologies = variables['technologies']
    output_streams = variables['output_streams']
    energy_input = variables['energy_input']
    conversion_efficiency = variables['CONVERSION_EFFICIENCY']
    omv_costs = variables['OMV_COSTS']

    calculated_maintenance_cost = 0
    for t in range(0, time):
        for tech in technologies:
            for energy in output_streams:
                calculated_maintenance_cost += (energy_input[t][tech]
                        * conversion_efficiency[tech][energy]
                        * omv_costs[tech])

    maintenance_cost = round(maintenance_cost, 3)
    calculated_maintenance_cost = round(calculated_maintenance_cost, 3)

    assert maintenance_cost == calculated_maintenance_cost


def test_check_total_cost():
    """ Ensure total cost is equal to the maintenance+operating+investment cost
    with multiple excel files """

    excel_files = ['storages_of_same_type.xlsx', 'exported_streams.xlsx', 'imported_streams.xlsx', 'storage.xlsx',
                   'fixed_capital_costs.xlsx', 'pv.xlsx', 'elec_and_heat_demands.xlsx', 'chp.xlsx',
                   'storage_looping.xlsx']
    for excel in excel_files:
        results = calc_results(excel)
        variables = results['solution']

        maintenance_cost = variables['maintenance_cost']
        operating_cost = variables['operating_cost']
        investment_cost = variables['investment_cost']
        total_cost = variables['total_cost']

        # assert total_cost >= 0
        # assert maintenance_cost >= 0
        # assert operating_cost >= 0
        assert investment_cost >= 0
        assert total_cost == maintenance_cost+operating_cost+investment_cost, f"\n " \
            f"Failed for the following excel file: {excel}"


def test_total_carbon():
    """Ensure that the total carbon is correct. total carbon = total carbon emissions - total carbon credits
    for several excel input files"""

    excel_files = ['test_file.xlsx', 'capacity_bounds.xlsx', 'imported_streams.xlsx',
                   'fixed_capital_costs.xlsx', 'pv.xlsx', 'elec_and_heat_demands.xlsx', 'chp.xlsx',
                   'storage_looping.xlsx']

    for excel in excel_files:
        results = calc_results(excel)
        variables = results['solution']

        total_carbon = variables['total_carbon']
        export_streams = variables['export_streams']
        import_streams = variables['import_streams']
        CARBON_FACTOR = variables['CARBON_FACTORS']
        CARBON_CREDIT = variables['CARBON_CREDITS']
        energy_imported = variables['energy_imported']
        energy_exported = variables['energy_exported']
        time = len(variables['time'])

        total_carbon_emission = 0
        total_carbon_credit = 0

        for stream in import_streams:
            carbon_factor = CARBON_FACTOR[stream]
            energy_used = sum(energy_imported[t][stream] for t in range(0, time))
            total_carbon_emission += carbon_factor * energy_used

        for stream in export_streams:
            carbon_credit = CARBON_CREDIT[stream]
            total_energy_exported = sum(energy_exported[t][stream] for t in range(0, time))
            total_carbon_credit += carbon_credit * total_energy_exported

        carbon = total_carbon_emission - total_carbon_credit
        calculated_carbon = round(carbon, 3)
        total_carbon = round(total_carbon, 3)

        assert total_carbon == calculated_carbon, f"\n " \
            f"Failed for the following excel file: {excel}"


def test_tech_energy_input_below_capacity():
    """
    Ensure tech energy input is below the capacity of the tech (converter) and positive
    """
    file = 'energy_input_below_capacity.xlsx'
    results = calc_results(file)
    variables = results['solution']

    technologies = variables['technologies']
    capacities = variables['capacities']
    energy_input = variables['energy_input']
    time = len(variables['time'])

    for tech in technologies:
        capacity = capacities[tech]
        for t in range(0, time):
            energy_inputted = energy_input[t][tech]

            assert energy_inputted <= capacity
            assert energy_inputted >= 0


def test_part_load_works():
    """ Ensure that part loads (CHP, MicroCHP) work """

    file = 'part_load.xlsx'
    results = calc_results(file)
    variables = results['solution']

    part_load = variables['PART_LOAD']

    assert part_load['CHP']['Heat'] == 0.5

    assert part_load['MicroCHP']['Elec'] == 0.5
    assert part_load['MicroCHP']['Heat'] == 0.5

    assert variables['MicroCHP'] == 3.24619
    assert variables['CHP'] == 10.0514

    energy_input = variables['energy_input']
    for t in range(0, 12):
        assert energy_input[t]['CHP'] == 10.0514

    energy = [0, 2.54472, 3.24619, 3.24619, 2.73756, 3.23812, 3.24619, 1.80344,
              2.63938, 3.24619, 3.24619, 3.24619]
    for t, value in enumerate(energy):
        assert energy_input[t]['MicroCHP'] == value

    assert variables['part_load'] == ['MicroCHP', 'CHP']

    is_on = variables['is_on']
    for t in range(0, 12):
        assert is_on[t]['CHP'] == 1
        if t == 0:
            assert is_on[t]['MicroCHP'] == 0
        else:
            assert is_on[t]['MicroCHP'] == 1

    is_installed = variables['is_installed']
    assert is_installed['CHP'] == 1
    assert is_installed['MicroCHP'] == 1


def test_tech_is_installed_works():
    """ Ensure tech_installed works """

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    assert variables['technologies'] == ['Grid', 'HP', 'Boiler', 'MicroCHP',
                                         'PV', 'ST', 'CHP', 'GSHP']

    tech_is_installed = variables['is_installed']
    assert tech_is_installed['Boiler'] == 1
    assert tech_is_installed['CHP'] == 1
    assert tech_is_installed['GSHP'] == 0
    assert tech_is_installed['Grid'] == 1
    assert tech_is_installed['HP'] == 0
    assert tech_is_installed['MicroCHP'] == 1
    assert tech_is_installed['PV'] == 1
    assert tech_is_installed['ST'] == 0

    assert variables['GSHP'] == 0
    assert variables['HP'] == 0
    assert variables['ST'] == 0

    assert variables['PV'] == 1
    assert variables['Boiler'] == 10
    assert variables['CHP'] == 5
    assert variables['Grid'] == 2.68114
    assert variables['MicroCHP'] == 1.4654


def test_storage_is_installed_works():
    """ Ensure storage installed works """

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    assert variables['storages'] == ['Battery', 'Hot Water Tank']

    storage_is_installed = variables['is_installed_2']
    assert storage_is_installed['Battery'] == 0
    assert storage_is_installed['Hot Water Tank'] == 1

    assert variables['Battery'] == 0
    assert variables['Hot Water Tank'] == 21.0085


def test_part_load_is_on():
    """ Ensure is_on for part load works"""

    file = 'part_load.xlsx'
    results = calc_results(file)
    variables = results['solution']

    assert variables['part_load'] == ['MicroCHP', 'CHP']

    is_on = variables['is_on']
    for t in range(0, 12):
        assert is_on[t]['CHP'] == 1
        if t == 0:
            assert is_on[t]['MicroCHP'] == 0
        else:
            assert is_on[t]['MicroCHP'] == 1


def test_storage_level_below_capacity():
    """ Ensure that storage level below capacity at all times """

    file = 'storage_level_.xlsx'
    results = calc_results(file)
    variables = results['solution']

    storages = variables['storages']
    assert storages == ['Battery', 'Hot Water Tank']

    storage_level = variables['storage_level']
    storage_capacity = variables['storage_capacity']

    for storage in storages:
        capacity = storage_capacity[storage]
        for t in range(0, 13):
            level = storage_level[t][storage]
            assert level <= capacity


def test_storage_level_above_min():
    """ Ensure storage level above minimum and positive at all times  """

    file = 'storage_level_.xlsx'
    results = calc_results(file)
    variables = results['solution']

    storages = variables['storages']
    assert storages == ['Battery', 'Hot Water Tank']

    storage_level = variables['storage_level']
    storage_capacity = variables['storage_capacity']
    MIN_STATE_OF_CHARGE = variables['MIN_STATE_OF_CHARGE']

    for storage in storages:
        capacity = storage_capacity[storage]
        min_state_of_charge = MIN_STATE_OF_CHARGE[storage]
        for t in range(0, 13):
            level = storage_level[t][storage]
            assert capacity * min_state_of_charge <= level


def test_storage_level_positive_with_no_min():
    """Ensure storage level is positive when there is no min storage level set
    and ensure that storage level can reach 0 if there is no min """

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']
    time = len(variables['time'])

    storages = variables['storages']
    storage_level = variables['storage_level']

    for storage in storages:
        for t in range(0, time):
            level = storage_level[t][storage]
            assert level >= 0

    for t in range(0, time):
        level = storage_level[t]['Battery']
        assert level == 0

    assert storage_level[7]['Hot Water Tank'] == 0


def test_capacity_bounds():
    """Ensure capacities are withing their bounds for both tech and storage """

    file = 'capacity_bounds.xlsx'
    results = calc_results(file)
    variables = results['solution']
    model = the_model(file)

    technologies = variables['technologies']
    storages = variables['storages']

    # Upper and lower bounds set in the input

    for tech in technologies:
        capacities = model._data._get_capacity(tech)
        lower_bound = capacities['bounds']['lower']
        upper_bound = capacities['bounds']['upper']
        capacity = variables[tech]
        assert capacity <= upper_bound
        assert capacity >= lower_bound

    for storage in storages:
        capacities = model._data._get_capacity(storage)
        lower_bound = capacities['bounds']['lower']
        upper_bound = capacities['bounds']['upper']
        capacity = variables[storage]
        assert capacity <= upper_bound
        assert capacity >= lower_bound

    # Only lower bound set in the input
    file = 'capacity_bounds_lower_bound.xlsx'
    results = calc_results(file)
    variables = results['solution']
    model = the_model(file)

    technologies = variables['technologies']
    storages = variables['storages']

    for tech in technologies:
        capacities = model._data._get_capacity(tech)
        lower_bound = capacities['bounds']['lower']
        capacity = variables[tech]
        assert capacity >= lower_bound

    for storage in storages:
        capacities = model._data._get_capacity(storage)
        lower_bound = capacities['bounds']['lower']
        capacity = variables[storage]
        assert capacity >= lower_bound

    # Only upper bound set in the input
    file = 'capacity_bounds_upper_bound.xlsx'
    results = calc_results(file)
    variables = results['solution']
    model = the_model(file)

    technologies = variables['technologies']
    storages = variables['storages']
    for tech in technologies:
        capacities = model._data._get_capacity(tech)
        upper_bound = capacities['bounds']['upper']
        capacity = variables[tech]
        assert capacity <= upper_bound
        assert capacity >= 0

    for storage in storages:
        capacities = model._data._get_capacity(storage)
        upper_bound = capacities['bounds']['upper']
        capacity = variables[storage]
        assert capacity <= upper_bound
        assert capacity >= 0


def test_tech_export_energy_positive():
    """Ensure exported energy from exported streams is positive """

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    export_streams = variables['export_streams']
    assert export_streams == ['PV_Elec']

    energy_exported = variables['energy_exported']
    for t in range(0, 11):
        assert energy_exported[t]['PV_Elec'] >= 0


def test_tech_import_energy_positive():
    """ Ensure energy imported from streams is positive """

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    import_streams = variables['import_streams']
    energy_imported = variables['energy_imported']

    for streams in import_streams:
        for t in range(0, 11):
            assert energy_imported[t][streams] >= 0


def test_energy_from_storage_positive():
    """Ensure energy from storage always positive"""

    file = 'storage_level_.xlsx'
    results = calc_results(file)
    variables = results['solution']

    storages = variables['storages']
    energy_from_storage = variables['energy_from_storage']

    for storage in storages:
        for t in range(0, 12):
            assert energy_from_storage[t][storage] >= 0


def test_energy_to_storage_positive():
    """Ensure energy to storage always positive """

    file = 'storage_level_.xlsx'
    results = calc_results(file)
    variables = results['solution']

    storages = variables['storages']
    energy_to_storage = variables['energy_to_storage']

    for storage in storages:
        for t in range(0, 12):
            assert energy_to_storage[t][storage] >= 0


def test_storage_discharge_rate():
    """Ensure storage discharge rate smaller or equal to maximum discharge rate of the storage"""

    file = 'storage_level_.xlsx'
    results = calc_results(file)
    variables = results['solution']

    storages = variables['storages']
    energy_from_storage = variables['energy_from_storage']
    MAX_DISCHARGE_RATE = variables['MAX_DISCHARGE_RATE']
    storage_capacity = variables['storage_capacity']

    time = len(variables['time'])

    for storage in storages:
        capacity = storage_capacity[storage]
        max_discharge_rate = MAX_DISCHARGE_RATE[storage]
        for t in range(0, time):
            discharge_rate = energy_from_storage[t][storage]
            assert discharge_rate <= (capacity * max_discharge_rate)


def test_storage_charge_rate():
    """Ensure storage charge rate is smaller or equal to maximum charge rate"""

    file = 'storage_level_.xlsx'
    results = calc_results(file)
    variables = results['solution']

    storages = variables['storages']
    energy_to_storage = variables['energy_to_storage']
    MAX_CHARGE_RATE = variables['MAX_CHARGE_RATE']
    storage_capacity = variables['storage_capacity']

    time = len(variables['time'])

    for storage in storages:
        capacity = storage_capacity[storage]
        max_charge_rate = MAX_CHARGE_RATE[storage]
        for t in range(0, time):
            discharge_rate = energy_to_storage[t][storage]
            assert discharge_rate <= (capacity * max_charge_rate)


def test_energy_balance():
    """Ensure loads and exported energy below the produced energy"""

    file = 'test_file.xlsx'
    results = calc_results(file)
    variables = results['solution']

    demands = variables['demands']
    streams = variables['streams']
    loads = variables['LOADS']
    energy_input = variables['energy_input']
    technologies = variables['technologies']
    conversion_efficiency = variables['CONVERSION_EFFICIENCY']
    imported_streams = variables['import_streams']
    exported_streams = variables['export_streams']
    energy_imported = variables['energy_imported']
    energy_exported = variables['energy_exported']
    storages = variables['storages']
    energy_from_storage = variables['energy_from_storage']
    energy_to_storage = variables['energy_to_storage']
    time = len(variables['time'])

    total_q_out = 0
    total_q_in = 0
    energy_out = 0

    for stream in streams:
        for t in range(0, time):
            if stream in demands:
                load = loads[stream][t]
            else:
                load = 0
            if stream in imported_streams:
                energy_import = energy_imported[t][stream]
            else:
                energy_import = 0
            if stream in exported_streams:
                energy_export = energy_exported[t][stream]
            else:
                energy_export = 0
            for tech in technologies:
                energy_out += (energy_input[t][tech]) * (conversion_efficiency[tech][stream])
            for storage in storages:
                total_q_out += energy_from_storage[t][storage]
                total_q_in += energy_to_storage[t][storage]

            assert load <= energy_out + total_q_out + energy_import - total_q_in - energy_export


def test_storage_balance():
    """Ensure next storge level claculated correctly"""

    file = 'storage_level_.xlsx'
    results = calc_results(file)
    variables = results['solution']

    charging_efficiency = variables['CHARGING_EFFICIENCY']
    discharging_efficiency = variables['DISCHARGING_EFFICIENCY']
    storage_level = variables['storage_level']
    storages = variables['storages']
    energy_from_storage = variables['energy_from_storage']
    energy_to_storage = variables['energy_to_storage']
    storage_standing_losses = variables['STORAGE_STANDING_LOSSES']
    time = len(variables['time'])

    for storage in storages:
        for t in range(0, time-1):
            current_level = storage_level[t][storage]
            next_level = storage_level[t+1][storage]

            calculated_next_level = ((1 - storage_standing_losses[storage])*current_level
                                     + (charging_efficiency[storage]*energy_to_storage[t][storage])
                                     - ((1/discharging_efficiency[storage])*energy_from_storage[t][storage])
                                     )

            next_level = round(next_level, 3)
            calculated_next_level = round(calculated_next_level, 3)

            assert next_level == calculated_next_level


def test_simple_model_solved_by_hand():
    """Checks that the EhubModel works with a simple model solved by hand """

    file = 'example_by_hand.xlsx'
    results = calc_results(file)
    variables = results['solution']

    energy_exported = variables['energy_exported']
    energy_input = variables['energy_input']
    energy_imported = variables['energy_imported']
    operating_cost = variables['operating_cost']
    investment_cost = variables['investment_cost']
    total_cost = variables['total_cost']
    export_streams = variables['export_streams']
    import_streams = variables['import_streams']
    streams = variables['streams']
    output_streams = variables['output_streams']

    assert investment_cost == 1250
    assert operating_cost == 22
    assert total_cost == 1272

    assert streams == ['Elec', 'Grid'] or ['Grid', 'Elec']
    assert output_streams == ['Elec']
    assert export_streams == ['Elec']
    assert import_streams == ['Grid']

    assert energy_exported[0]['Elec'] == 10
    for t in [1, 2]:
        assert energy_exported[t]['Elec'] == 0

    assert energy_imported[0]['Grid'] == 0
    assert energy_imported[1]['Grid'] == 60
    assert energy_imported[2]['Grid'] == 40

    assert energy_input[0]['PV'] == 50
    assert energy_input[1]['PV'] == 15
    assert energy_input[2]['PV'] == 25

def test_data_as_time_series():
    """Insures that import price,export price, co2 factors and co2 credits can be inputted as only time series data or
    partly as time series and as a parameter """

    file1 = 'no_time_series.xlsx'
    results1 = calc_results(file1)
    variables1 = results1['solution']

    file2 = 'time_series.xlsx'
    results2 = calc_results(file2)
    variables2 = results2['solution']

    file3 = 'mixed_time_series.xlsx'
    results3 = calc_results(file3)
    variables3 = results3['solution']

    energy_exported1 = variables1['energy_exported']
    energy_input1 = variables1['energy_input']
    energy_imported1 = variables1['energy_imported']
    operating_cost1 = variables1['operating_cost']
    investment_cost1 = variables1['investment_cost']
    maintenance_cost1 = variables1['maintenance_cost']
    total_cost1 = variables1['total_cost']
    total_carbon1 = variables1['total_carbon']

    energy_exported2 = variables2['energy_exported']
    energy_input2 = variables2['energy_input']
    energy_imported2 = variables2['energy_imported']
    operating_cost2 = variables2['operating_cost']
    investment_cost2 = variables2['investment_cost']
    maintenance_cost2 = variables2['maintenance_cost']
    total_cost2 = variables2['total_cost']
    total_carbon2 = variables2['total_carbon']

    energy_exported3 = variables3['energy_exported']
    energy_input3 = variables3['energy_input']
    energy_imported3 = variables3['energy_imported']
    operating_cost3 = variables3['operating_cost']
    investment_cost3 = variables3['investment_cost']
    maintenance_cost3 = variables3['maintenance_cost']
    total_cost3 = variables3['total_cost']
    total_carbon3 = variables3['total_carbon']

    export_streams = variables1['export_streams']
    import_streams = variables1['import_streams']
    technologies= variables1['technologies']
    time = len(variables1['time'])

    assert maintenance_cost1 == maintenance_cost2 == maintenance_cost3
    assert operating_cost1 == operating_cost2 == operating_cost3
    assert investment_cost1 == investment_cost2 == investment_cost3
    assert total_cost1 == total_cost2 == total_cost3
    assert total_carbon1 == total_carbon2 == total_carbon3

    for stream in export_streams:
        for t in range(time):
            eng_export1 = energy_exported1[t][stream]
            eng_export2 = energy_exported2[t][stream]
            eng_export3 = energy_exported3[t][stream]

            assert eng_export1 == eng_export2 == eng_export3

    for stream in import_streams:
        for t in range(time):
            eng_import1 = energy_imported1[t][stream]
            eng_import2 = energy_imported2[t][stream]
            eng_import3 = energy_imported3[t][stream]

            assert eng_import1 == eng_import2 == eng_import3

    for tech in technologies:
        for t in range(time):
            eng_input1 = energy_input1[t][tech]
            eng_input2 = energy_input2[t][tech]
            eng_input3 = energy_input3[t][tech]

            assert eng_input1 == eng_input2 == eng_input3

def test_multiple_sources():
    """Test that the model can use more than one source"""

    file = 'multiple_sources.xlsx'
    results = calc_results(file)
    variables = results['solution']

    technologies = variables['technologies']
    capacity = variables['capacity_tech']
    is_installed = variables['is_installed']

    for tech in technologies:
        assert is_installed[tech] == 1
        assert capacity[tech] != 0

    assert capacity['Grid'] == 1.55
    assert capacity['PV1'] == 6.4592
    assert capacity['PV2'] == 5
    assert capacity['PV3'] == 1.36
