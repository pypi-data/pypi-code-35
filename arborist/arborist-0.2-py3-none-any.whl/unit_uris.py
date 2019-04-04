from .filesystem import write_graph
from .graph_common import add_common_elements
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDFS


def generate_unit_uris(output_base_dir):
    """Note the URIs needed for units. They all come from the Ontology of Units
    of Measure."""
    output_base_dir = Path(output_base_dir)

    units = [(
        'kilogram',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/kilogram',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/PrefixedUnit',
    ), (
        'megajoule',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/megajoule',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/PrefixedUnit',
    ), (
        'euro',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/euro',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/Unit',
    ), (
        'hectare',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/hectare',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/PrefixedUnit',
    ), (
        'cubic meters',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/cubicMetre',
        'http://www.ontology-of-units-of-measure.org/resource/om-2/UnitExponentiation'
    )]

    g = add_common_elements(
        Graph(),
        base_uri="http://rdf.bonsai.uno/unit/",
        title="Unit definitions used in BONSAI",
        description="Units from ontology-of-units-of-measure used in BONSAI",
        author="Chris Mutel",
        version="0.2",
    )
    g.bind('om2', 'http://www.ontology-of-units-of-measure.org/resource/om-2/')

    for label, uri, kind in units:
        node = URIRef(uri)
        g.add((node, RDF.type, URIRef(kind)))
        g.add((node, RDFS.label, Literal(label)))

    write_graph(output_base_dir / "unit", g)
