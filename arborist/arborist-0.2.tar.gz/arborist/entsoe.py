from .graph_common import generate_generic_graph
from pathlib import Path


def generate_entsoe_uris(output_base_dir):
    data = [
        ('Fossil Hard coal', 'fhc'),
        ('Fossil Brown coal/Lignite', 'fbcl'),
        ('Fossil Gas', 'fg'),
        ('Fossil Coal-derived gas', 'fcg'),
        ('Nuclear', 'nuke'),
        ('Hydro Pumped Storage', 'ps'),
        ('Hydro Run-of-river and poundage', 'h2o'),
        ('Hydro Water Reservoir', 'res'),
        ('Wind Offshore', 'woff'),
        ('Wind Onshore', 'won'),
        ('Fossil Oil', 'fo'),
        ('Fossil Oil shale', 'fos'),
        ('Biomass', 'bio'),
        ('Fossil Peat', 'peat'),
        ('Waste', 'was'),
        ('Solar', 'sun'),
        ('Other renewable', 'othr'),
        ('Geothermal', 'geo'),
        ('Other', 'oth'),
        ('Marine', 'mar'),
    ]

    generate_generic_graph(
        Path(output_base_dir),
        kind='ActivityType',
        data=data,
        directory_structure=["entsoe"],
        title="ENTSO-E activity types",
        description='ENTSO-E activity types used in BONSAI modelling',
        author="Chris Mutel",
        version="0.2",
    )
