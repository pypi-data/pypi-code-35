"""Generate the URIs needed for core activity type `electricity grid`.
Handcrafted as not available elsewhere."""
from .graph_common import generate_generic_graph


def generate_electricity_grid_uris(output_base_dir):
    generate_generic_graph(
        output_base_dir,
        kind='ActivityType',
        data=[
            ("Electricity grid", "eg"),
        ],
        directory_structure=["core", "electricity_grid"],
        title="Electricity grid activity types for BONSAI",
        description='ActivityType instances needed for BONSAI electricity grid modelling',
        author="Arthur Jakobs",
        version="0.2",
    )

    generate_generic_graph(
        output_base_dir,
        kind='FlowObject',
        data=[
            ("Electricity", "elec"),
        ],
        directory_structure=["core", "electricity_grid"],
        title="Electricity grid flow objects for BONSAI",
        description='FlowObject instances needed for BONSAI electricity grid modelling',
        author="Arthur Jakobs",
        version="0.3",
    )
