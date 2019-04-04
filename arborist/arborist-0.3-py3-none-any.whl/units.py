from .filesystem import create_dir
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS


def generate_unit_uris(output_base_dir):
    """Note the URIs needed for units. They all come from the Ontology of Units
    of Measure."""
    output_base_dir = Path(output_base_dir)

    om2 = Namespace("http://www.ontology-of-units-of-measure.org/resource/om-2/")

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

    g = Graph()
    g.bind('om2', 'http://www.ontology-of-units-of-measure.org/resource/om-2/')

    for label, uri, kind in units:
        node = URIRef(uri)
        g.add( (node, RDF.type, URIRef(kind)) )
        g.add( (node, RDFS.label, Literal(label)) )

    create_dir(output_base_dir / "unit")
    with open(
            output_base_dir / "unit" / "unit.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')




