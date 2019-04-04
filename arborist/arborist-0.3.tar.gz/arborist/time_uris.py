from .filesystem import write_graph
from .graph_common import add_common_elements
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS, OWL, XSD


def generate_time_uris(output_base_dir):
    """Time URIs used for now. Hard coded because no external data to consume."""
    output_base_dir = Path(output_base_dir)

    WIKIDATA_MAPPING = {
        2010: "https://www.wikidata.org/wiki/Q1995",
        2011: "https://www.wikidata.org/wiki/Q1994",
        2012: "https://www.wikidata.org/wiki/Q1990",
        2013: "https://www.wikidata.org/wiki/Q1998",
        2014: "https://www.wikidata.org/wiki/Q1999",
        2015: "https://www.wikidata.org/wiki/Q2002",
        2016: "https://www.wikidata.org/wiki/Q25245",
        2017: "https://www.wikidata.org/wiki/Q25290",
        2018: "https://www.wikidata.org/wiki/Q25291",
        2019: "https://www.wikidata.org/wiki/Q25274",
        2020: "https://www.wikidata.org/wiki/Q25337",
    }

    owltime = Namespace("https://www.w3.org/TR/owl-time/")

    g = add_common_elements(
        Graph(),
        base_uri='http://rdf.bonsai.uno/time/',
        title="Years 2010 - 2020",
        description="Complete years 2010 - 2020 for use in BONSAI",
        author='Chris Mutel',
        version="0.2"
    )

    g.bind('brdftime', 'http://rdf.bonsai.uno/time/')

    oneyear = URIRef("brdftime:oneyearlong")
    g.add((oneyear, RDF.type, owltime.DurationDescription))
    g.add((oneyear, owltime.years, Literal("1", datatype=XSD.integer)))

    for year, wd in WIKIDATA_MAPPING.items():
        end = URIRef("brdftime:{}end".format(year))
        g.add((end, RDF.type, owltime.Instant))
        g.add((end, owltime.inXSDDate, Literal("{}-12-31".format(year), datatype=XSD.date)))

        begin = URIRef("brdftime:{}start".format(year))
        g.add((begin, RDF.type, owltime.Instant))
        g.add((begin, owltime.inXSDDate, Literal("{}-01-01".format(year), datatype=XSD.date)))

        node = URIRef("brdftime:{}".format(year))
        g.add((node, RDF.type, owltime.ProperInterval))
        g.add((node, RDFS.label, Literal(year)))
        g.add((node, owltime.hasBeginning, begin))
        g.add((node, owltime.hasEnd, end))
        g.add((node, owltime.hasDurationDescription, oneyear))
        g.add((node, owltime.inXSDDate, Literal("{}-01-01".format(year), datatype=XSD.date)))
        g.add((node, OWL.sameAs, URIRef(wd)))
        g.add((node, OWL.sameAs, URIRef("http://reference.data.gov.uk/doc/year/{}".format(year))))

    write_graph(output_base_dir / "time", g)
