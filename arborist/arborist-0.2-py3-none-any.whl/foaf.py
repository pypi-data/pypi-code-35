from .filesystem import write_graph
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS


def generate_foaf_uris(output_base_dir):
    """Note the URIs needed for units. They all come from the Ontology of Units
    of Measure."""
    output_base_dir = Path(output_base_dir)

    org = Namespace("https://www.w3.org/TR/vocab-org/")

    g = Graph()
    g.bind('org', 'https://www.w3.org/TR/vocab-org/')
    g.bind('skos', SKOS)
    g.bind('foaf', FOAF)

    node = URIRef("http://bonsai.uno/foaf/foaf.ttl#bonsai")
    g.add((node, RDF.type, org.Organization))
    g.add((node, SKOS.prefLabel, Literal("BONSAI – Big Open Network for Sustainability Assessment Information")))
    g.add((node, FOAF.homepage, URIRef("http://bonsai.uno")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q131201")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q2323664")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q18692990")))

    write_graph(output_base_dir / "foaf", g)
