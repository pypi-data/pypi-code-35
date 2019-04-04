"""Generate the URIs needed for modelling the effects of climate change.
This code creates both `activityTypes` and `flowObjects`.

As these are not present in any online data, we have hard coded our own URIs"""
from .graph_common import generate_generic_graph


def generate_climate_change_uris(output_base_dir):
    generate_generic_graph(
        output_base_dir,
        kind='ActivityType',
        data=[
            ("Atmospheric energy balance",),
            ("Temperature increase",),
        ],
        directory_structure=["lcia", "climate_change"],
        title="Climate change activity types",
        description='ActivityType instances needed for BONSAI climate change modelling',
        author="Tiago Morais",
        version="0.3",
    )

    generate_generic_graph(
        output_base_dir,
        kind='FlowObject',
        data=[
            ("Radiative forcing",),
            ("Temperature increase - 100 year horizon",
             "temperature_increase_100yr_horizon"),
        ],
        directory_structure=["lcia", "climate_change"],
        title="Climate change activity types",
        description='FlowObject instances needed for BONSAI climate change modelling',
        author="Tiago Morais",
        version="0.3",
    )
