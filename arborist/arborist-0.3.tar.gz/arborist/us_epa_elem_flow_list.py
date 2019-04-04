"""Generate the URIs needed for US EPA elementary flow list.
This code creates both `flowObjects`.
As these are not present in any online data, we have hard coded our own URIs"""
from . import data_dir
from .filesystem import write_graph
from .graph_common import NS, add_common_elements
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS, OWL
import pandas


def generate_us_epa_uris(output_base_dir):
    data = pandas.read_csv(data_dir / 'USEPA_URI.csv')
    output_base_dir = Path(output_base_dir)

    uri = "http://rdf.bonsai.uno/flowobject/us_epa_elem/"
    epa_ns = Namespace(uri)

    g = add_common_elements(
        Graph(),
        base_uri=uri,
        title="US EPA Elementary Flow List",
        description="US EPA Elementary Flow List from https://github.com/USEPA/Federal-LCA-Commons-Elementary-Flow-List",
        author="Tiago Morais",
        version="0.3 (2019-04-03)",
    )
    g.bind('brdffo', uri)

    for label, code in data.values:
        node = URIRef(epa_ns[code])
        g.add((node, RDF.type, NS.nb.FlowObject))
        g.add((node, OWL.sameAs, URIRef("http://www.chemspider.com/{}".format(code))))
        g.add((node, RDFS.label, Literal(label)))

    write_graph(
        output_base_dir / "flowobject" / "us_epa_elem",
        g
    )
