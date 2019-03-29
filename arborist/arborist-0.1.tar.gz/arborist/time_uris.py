from .filesystem import create_dir
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS, OWL, XSD


def generate_time_uris(output_base_dir):
    """Time URIs used for now. Hard coded because no external data to consume."""
    output_base_dir = Path(output_base_dir)

    WIKIDATA_MAPPING = {
        2011: "https://www.wikidata.org/wiki/Q1994",
        2015: "https://www.wikidata.org/wiki/Q2002",
        2016: "https://www.wikidata.org/wiki/Q25245",
        2017: "https://www.wikidata.org/wiki/Q25290",
        2018: "https://www.wikidata.org/wiki/Q25291",
    }

    nb = Namespace("http://ontology.bonsai.uno/core#")
    owltime = Namespace("https://www.w3.org/TR/owl-time/")
    nbt = Namespace("http://rdf.bonsai.uno/time/")

    g = Graph()
    g.bind('bont', 'http://ontology.bonsai.uno/core#')
    g.bind('brdftime', 'http://rdf.bonsai.uno/time/')
    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("xsd", XSD)
    g.bind("ot", "https://www.w3.org/TR/owl-time/")

    oneyear = URIRef("brdftime:oneyearlong")
    g.add( (oneyear, RDF.type, owltime.DurationDescription) )
    g.add( (oneyear, owltime.years, Literal("1", datatype=XSD.integer)) )

    for year, wd in WIKIDATA_MAPPING.items():
        end = URIRef("brdftime:{}end".format(year))
        g.add( (end, RDF.type, owltime.Instant) )
        g.add( (end, owltime.inXSDDate, Literal("{}-12-31".format(year), datatype=XSD.date)))

        begin = URIRef("brdftime:{}start".format(year))
        g.add( (begin, RDF.type, owltime.Instant) )
        g.add( (begin, owltime.inXSDDate, Literal("{}-01-01".format(year), datatype=XSD.date)))

        node = URIRef("brdftime:{}".format(year))
        g.add( (node, RDF.type, owltime.ProperInterval) )
        g.add( (node, RDFS.label, Literal(year)) )
        g.add( (node, owltime.hasBeginning, begin))
        g.add( (node, owltime.hasEnd, end))
        g.add( (node, owltime.hasDurationDescription, oneyear))
        g.add( (node, owltime.inXSDDate, Literal("{}-01-01".format(year), datatype=XSD.date)))
        g.add( (node, OWL.sameAs, URIRef(wd)))
        g.add( (node, OWL.sameAs, URIRef("http://reference.data.gov.uk/doc/year/{}".format(year))))
        g.add( (node, DC.title, Literal("Year {}".format(year))) )
        g.add( (node, DC.description, Literal("The complete year {}".format(year))) )
        g.add( (node, DC.publisher, Literal("bonsai.uno")) )
        g.add( (node, DC.creator, URIRef("http://bonsai.uno/foaf/bonsai.rdf#bonsai")) )
        g.add( (node, DC.contributor, Literal("Chris Mutel")) )
        g.add( (node, URIRef("http://creativecommons.org/ns#license"), URIRef('http://creativecommons.org/licenses/by/3.0/')) )

    create_dir(output_base_dir / "time")
    with open(
            output_base_dir / "time" / "time.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')
