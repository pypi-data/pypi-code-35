from arborist import get_metadata
from bentso.iterators import iterate_generation, iterate_trade, COUNTRIES
from itertools import count
from pathlib import Path
import itertools
import json
import numpy as np
import os
import tarfile
import tempfile


# Generated from
# https://github.com/BONSAMURAIS/Correspondence-tables/blob/master/final_tables/tables/exiobase_to_bentso_activities.csv
# And supplemented by missing key errors :)
ACTIVITY_MAPPING = {
    'Fossil Hard coal': 'Production of electricity by coal',
    'Fossil Brown coal/Lignite': 'Production of electricity by coal',
    'Fossil Gas': 'Production of electricity by gas',
    'Fossil Coal-derived gas': 'Production of electricity by gas',
    'Nuclear': 'Production of electricity by nuclear',
    'Hydro Pumped Storage': 'Production of electricity by hydro',
    'Hydro Run-of-river and poundage': 'Production of electricity by hydro',
    'Hydro Water Reservoir': 'Production of electricity by hydro',
    'Wind Offshore': 'Production of electricity by wind',
    'Wind Onshore': 'Production of electricity by wind',
    'Fossil Oil': 'Production of electricity by petroleum and other oil derivatives',
    'Fossil Oil shale': 'Production of electricity by petroleum and other oil derivatives',
    'Biomass': 'Production of electricity by biomass and waste',
    'Fossil Peat': 'Production of electricity by coal',
    'Waste': 'Production of electricity by biomass and waste',
    'Solar': 'Production of electricity by solar thermal',
    'Other renewable': 'Production of electricity by tide, wave, ocean',
    'Geothermal': 'Production of electricity by Geothermal',
    'Other': 'Production of electricity nec',
    'Marine': 'Production of electricity nec',
    'Grid': "Market for Electricity",
}
FLOW_MAPPING = {
    'Fossil Hard coal': 'Electricity by coal',
    'Fossil Brown coal/Lignite': 'Electricity by coal',
    'Fossil Gas': 'Electricity by gas',
    'Fossil Coal-derived gas': 'Electricity by gas',
    'Nuclear': 'Electricity by nuclear',
    'Hydro Pumped Storage': 'Electricity by hydro',
    'Hydro Run-of-river and poundage': 'Electricity by hydro',
    'Hydro Water Reservoir': 'Electricity by hydro',
    'Wind Offshore': 'Electricity by wind',
    'Wind Onshore': 'Electricity by wind',
    'Fossil Oil': 'Electricity by petroleum and other oil derivatives',
    'Fossil Oil shale': 'Electricity by petroleum and other oil derivatives',
    'Biomass': 'Electricity by biomass and waste',
    'Fossil Peat': 'Electricity by coal',
    'Waste': 'Electricity by biomass and waste',
    'Solar': 'Electricity by solar thermal',
    'Other renewable': 'Electricity by tide; wave; ocean',
    'Geothermal': 'Electricity by Geothermal',
    'Other': 'Electricity nec',
    'Marine': 'Electricity nec',
    'Grid': "Electricity",
}


def convert_entsoe_to_numpy(year, rdf_base_dir):
    metadata = get_metadata(rdf_base_dir)

    nrows = len(COUNTRIES) * len(set(FLOW_MAPPING.values()))
    ncols = len(COUNTRIES) * len(set(ACTIVITY_MAPPING.values()))
    supply = np.zeros((nrows, ncols), dtype=np.float32)
    use = np.zeros((nrows, ncols), dtype=np.float32)

    sorted_flow_values = sorted(set(FLOW_MAPPING.values()))
    sorted_activity_values = sorted(set(ACTIVITY_MAPPING.values()))
    sorted_countries = sorted(COUNTRIES)

    col_mapping = {
        (x, y): i for i, (x, y) in enumerate(itertools.product(
        sorted_countries, sorted_activity_values))
    }
    row_mapping = {
        (x, y): i for i, (x, y) in enumerate(itertools.product(
        sorted_countries, sorted_flow_values))
    }

    # Get grid mixes
    for technology, country, amount in iterate_generation(year):
        supply[
            row_mapping[(country, FLOW_MAPPING[technology])],
            col_mapping[(country, ACTIVITY_MAPPING[technology])],
        ] += amount

    for technology, country, amount in iterate_generation(year):
        use[
            row_mapping[(country, FLOW_MAPPING[technology])],
            col_mapping[(country, ACTIVITY_MAPPING['Grid'])],
        ] += amount

    for from_, to_, amount in iterate_trade(year):
        use[
            row_mapping[(from_, FLOW_MAPPING['Grid'])],
            col_mapping[(to_, ACTIVITY_MAPPING['Grid'])],
        ] += amount

    with tempfile.TemporaryDirectory() as t:
        output_dir = Path(t)

        np.save(output_dir / "entsoe-supply.npy", supply)
        np.save(output_dir / "entsoe-use.npy", supply)

        rm_reverse = sorted([(v, k) for k, v in row_mapping.items()])
        cm_reverse = sorted([(v, k) for k, v in col_mapping.items()])
        with open(output_dir / "entsoe-products.json", "w", encoding='utf-8') as f:
            json.dump([x[1] for x in rm_reverse], f, ensure_ascii=False)
        with open(output_dir / "entsoe-activities.json", "w", encoding='utf-8') as f:
            json.dump([x[1] for x in cm_reverse], f, ensure_ascii=False)

        with tarfile.open("entsoe-beebee-{}.tar.bz2".format(year),
                          "w:bz2") as f:
            f.add(output_dir / "entsoe-supply.npy", "entsoe-supply.npy")
            f.add(output_dir / "entsoe-use.npy", "entsoe-use.npy")
            f.add(output_dir / "entsoe-activities.json", "entsoe-activities.json")
            f.add(output_dir / "entsoe-products.json", "entsoe-products.json")
