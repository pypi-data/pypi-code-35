import csv
from pathlib import Path
from rdflib import Graph, URIRef
from rdflib.namespace import RDFS

metadata_dir = Path(__file__).parent / "meta"


def get_turtle_labels(filepath):
    if isinstance(filepath, Path):
        filepath = filepath.absolute()

    g = Graph()
    g.parse(str(filepath), format="turtle")

    for x, y, z in g:
        if y == RDFS.label:
            # Flip to go from label to URI
            yield str(z), str(x)

def get_metadata(rdf_base):
    if not isinstance(rdf_base, Path):
        rdf_base = Path(rdf_base)

    metadata = {}

    _ = lambda x: x if x.startswith("http://") else "http://" + x

    exiobase_activity_types = dict(get_turtle_labels(
        rdf_base / "activitytype" / "exiobase3_3_17" / "exiobase3_3_17.ttl"
    ))
    grid_activity_types = dict(get_turtle_labels(
        rdf_base / "activitytype" / "core" / "electricity_grid" / "electricity_grid.ttl"
    ))

    metadata["activitytype"] = exiobase_activity_types
    metadata["activitytype"].update(grid_activity_types)

    metadata["flowobject"] = dict(get_turtle_labels(
        rdf_base / "flowobject" / "exiobase3_3_17" / "exiobase3_3_17.ttl"
    ))
    metadata["location"] = dict(get_turtle_labels(
        rdf_base / "location" / "exiobase3_3_17" / "exiobase3_3_17.ttl"
    ))
    metadata["unit"] = dict(get_turtle_labels(
        rdf_base / "unit" / "unit.ttl"
    ))
    metadata["time"] = dict(get_turtle_labels(
        rdf_base / "time" / "time.ttl"
    ))

    return metadata
