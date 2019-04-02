import time
import argparse
from pathlib import Path

from .distance import distance
from .geoindex import GeoIndex
from .table import Table


def cli():

    note1 = '---------------------------------------------------------------'
    note2 = 'Notes:'
    note3 = '- The --distance and --neigbor arguments can be repeated.'
    note4 = '\nExample:\n> tupu some_cities.csv \n\t-o augmented.csv \n\t-d dist_ny,40.71,-74.0 \n\t-d dist_dc,38.9,-77.0 \n\t-n dist_reserve,id_reserve,reserve_cities.tsv?id=feature_id\n\t-n dist_self,id_self'
    notes = '\n'.join((note1, note2, note3, note4, note1))

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description='tupu: calculate geodesic distances between points and sets', epilog=notes)
    parser.add_argument('filename')
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--timeit", help="report elapsed time", action="store_true")
    parser.add_argument('--output','-o', action='store', help='output filename; comma-separated for .csv files, else tab-separated', required=True)
    parser.add_argument('--distance','-d', action='append', help='compute distance to point <lat,lon> and store it in column <dist>: "dist,lat,lon"')
    parser.add_argument('--neighbor','-n', action='append', help='compute distance to closest point in <fn>, and store it in columns <dist,id>: "dist,id,fn". If <fn> is omitted, will compare against self (input filename)')
    args = parser.parse_args()

    verbose = args.verbose
    timeit = args.timeit
    if timeit: start_time = time.time()
    if verbose: print(' - Validating input...')

    # Parse input filename and load input data
    input_table = Table(args.filename, verbose=verbose)

    # Check that the output file has the correct extension
    out_fn = Path(args.output)
    assert out_fn.suffix in ('.raw', '.tsv', '.csv'), out_fn.suffix

    # Compute distances between each input row and given points
    for _ in args.distance:
        dist_name, lat, lon = validate_cli_distance(_)
        if verbose:
            print(f' - Computing distance to lat={lat} lon={lon} and storing it in "{dist_name}"')
            input_table.add_distance_to_point(lat, lon, dist_name)

    # Compute minimum distances between each input row and a given *set* of points
    for _ in args.neighbor:
        id_name, dist_name, fn = validate_cli_neighbor(_)

        if fn is None:
            # Distance to the list itself
            input_table.add_distance_to_self(id_name, dist_name)
        else:
            # Distance to another list
            neighbor_table = Table(fn, verbose=verbose)
            input_table.add_distance_to_table(neighbor_table, id_name, dist_name)

    # Save data        
    input_table.save(out_fn)
    
    # Done!
    if verbose:
        print('\nDone!')
    if timeit:
        print("--- {:7.3f} seconds ---".format(time.time() - start_time))


def validate_cli_distance(input):
    input = input.split(',')
    assert len(input) == 3, f'--distance requires a (name,lat,lon) list,  but received {input}'
    name, lat, lon = input
    lat = float(lat)
    lon = float(lon)
    assert -90 <= lat <= 90
    assert -180 <= lon <= 180
    return name, lat, lon


def validate_cli_neighbor(input):
    input = input.split(',')
    assert len(input) in (2,3), f'--neighbor requires either <id,dist,fn> or <id,dist>, but received {input}'
    if len(input) == 2:
        input.append(None)
    id_name, dist_name, fn = input
    return id_name, dist_name, fn
