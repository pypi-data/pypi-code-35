"""
Solving energy hub model for n number of hubs with any network of connections wanted.

To run for multiple hubs:
    $ python multiple_hubs.py -n NUMBER OF HUBS

Inputting the number of hubs(n) is necessary for the model to run.

Naming input excel files:
    file names should start with "hub" followed by increasing numbers.
    the files should be in the 'network' folder

To set the connections between the hubs:
    Should be done in the connections list in the code.
        ex: [(0,1)]
    The first number can only export to the other hub, the second number can only import from the other hub.

    For bidirectional connection, the connection should be defined both ways:
        ex: [(0,1),
             (1,0)]


(Do not name constraints specific names in the EHubModel class -> will not be able to construct constraints)
"""
import os
import pylp
import argparse

from pylp import RealVariable
from energy_hub import EHubModel
from energy_hub.utils import constraint
from outputter import print_section, output_excel


class NetworkModelWithTotalCarbon(EHubModel):
    """
    A subclass that allows connections between hubs.
    """

    MAX_CARBON=0

    def __init__(self, *, excel=None, request=None, name=None, n=0):
        super().__init__(excel=excel, request=request)
        if n is not None:
            self.MAX_CARBON = n
        self.name = name

    # A constraint for epsilon constraint method
    @constraint()
    def max_carbon_level(self):
        return self.total_carbon <= float(self.MAX_CARBON)

class NetworkModelWithoutTotalCarbon(EHubModel):
    """
    A subclass that allows connections between hubs.
    """

    def __init__(self, *, excel=None, request=None, name=None):
        super().__init__(excel=excel, request=request)
        self.name = name


@constraint()
def network_constraint(hub, link_end, link_start):
    """
    Yields the constraints that allow a network connection between two hubs.

    Args:
        hub: The hub
        link_end: all the links that the hub imports
        link_start: all the links that the hub exports
    Yields:
       An energy balanced constraints for each hub
    """

    for t in hub.time:
        link_starting = []
        link_ending = []

        for i in range(len(link_start)):
            link_starting.append(link_start[i][t])

        for i in range(len(link_end)):
            link_ending.append(link_end[i][t])

        yield(hub.energy_exported[t]['Net_export'] == sum(link_starting))
        yield(hub.energy_imported[t]['Net_import'] == sum(link_ending))


def multiple_hubs(minimize_carbon=False, output_filename=None, carbon_value=0, n=0):
    if carbon_value is None:
        carbon_value = 0

    # Create all the hubs
    hubs = []
    for i in range(0, n):
        file_name = f'network/hub{i + 1}.xlsx'

        # This is a cross-platform way of getting the path to the Excel file
        current_directory = os.path.dirname(os.path.realpath(__file__))
        excel_file = os.path.join(current_directory, file_name)

        if minimize_carbon:
            hub = NetworkModelWithTotalCarbon(excel=excel_file, name=f'hub{i+1}', n=carbon_value)
        else:
            hub = NetworkModelWithoutTotalCarbon(excel=excel_file, name=f'hub{i+1}')
        hubs.append(hub)

    constraints = []
    for hub in hubs:
        hub.recompile()
        for constr in hub.constraints:
            constraints.append(constr)

    # These are the indexes between the different hubs.
    connections = [
        (0,1),
        (0,2),
        (1,3),
        (2,3)
    ]

    links = []

    energy_flow = {
        t: {out: RealVariable() for out in range(len(connections))}
        for t in hubs[0].time
    }

    for i in range(len(connections)):
        hub = hubs[0]
        flow = []
        for t in hub.time:
            flow.append(energy_flow[t][i])

        links.insert(i, flow)

    # Create a network connection
    for k, hub in enumerate(hubs):
        link_start = []
        link_end = []

        for i in range(len(connections)):
            if connections[i][0] == k:
                link_start.append(links[i])
            if connections[i][1] == k:
                link_end.append(links[i])

        for c in network_constraint(hub, link_end, link_start):
            constraints.append(c)

    # The objective function of the model is the summation of all the hub's
    # objective function
    objective = hubs[0].objective

    for hub in hubs[1:]:
        objective += hub.objective

    # Now solve this model.
    status = pylp.solve(objective=objective, constraints=constraints, minimize=True)

    #: Define the different sheets that we output
    sheets = [
    	"Other",
   	"LOADS",
   	"SOLAR_EM",
   	"energy_exported",
   	"energy_from_storage",
   	"energy_imported",
   	"energy_to_storage",
   	"is_on",
   	"storage_level",
    "capacity_storage",
    "capacity_tech"
    ]

    #: Used to output files with names according to their job.
    if minimize_carbon:
        ext = "_minimized_carbon"
    else:
        ext = "_minimized_cost"

    #: A list used to return all dictionaries gathered from this function.
    hub_dict_list = []

    # Print out the hub's name and all stuff related to that model.
    tcar = 0
    tcost = 0
    for i, hub in enumerate(hubs):
        hub_dict_list.append(hub.solution_dict)
        if output_filename is None:
            output_excel(hub.solution_dict, f'{hub.name}{ext}.xlsx', sheets=sheets)
            print_section(f'{hub.name}{ext}', hub.solution_dict)
        else:
            output_excel(hub.solution_dict, f'{output_filename}_{i}{ext}.xlsx', sheets=sheets)
            print_section(f'{hub.name}_{i}{ext}', hub.solution_dict)
        tcar += hub.solution_dict["total_carbon"]
        tcost += hub.solution_dict["total_cost"]

    for i, hub in enumerate(hubs):
        half_heading = '=' * 4
        for t in hub.time:
            net_imp = hub.solution_dict['energy_imported'][t]['Net_import']
            net_exp = hub.solution_dict['energy_exported'][t]['Net_export']

            if (net_imp != 0) and (net_exp != 0):
                print(f"{half_heading} {'Warning:'} {half_heading} \n{'Export & import at the same time for hub: '} {i} "
                      f"{'; For time step: '} {t} ")

    print("\nAbsolute total carbon:\t" + str(tcar))
    print("Absolute total cost:\t" + str(tcost), end='\n\n')
    return hub_dict_list


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Command line utility to run tests.")
    parser.add_argument('-c', '--carbon', action='store_true', help='Optimize based on the total carbon level.')
    parser.add_argument('-o', '--output_filename', type=str, help='The name that the output should be stored under.')
    parser.add_argument('-v', '--carbon_value', type=float, help='The value that the carbon should try to be.')
    parser.add_argument('-n', '--number_of_hubs', type=int, help='The number of hubs to be used')

    args = parser.parse_args()

    multiple_hubs(args.carbon, args.output_filename, args.carbon_value, args.number_of_hubs)


