from . import data_dir
from .filesystem import create_dir
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS
import pandas


def generate_exiobase_metadata_uris(output_base_dir):
    output_base_dir = Path(output_base_dir)

    df = pandas.read_excel(
        data_dir / "exiobase_classifications_v_3_3_17.xlsx",
        sheet_name="Activities",
        header=0
    )
    data = set(zip(df['Activity name'], df['Activity code 2']))

    nat = Namespace("http://rdf.bonsai.uno/activitytype/exiobase3_3_17/")
    nb = Namespace("http://ontology.bonsai.uno/core#")
    nfo = Namespace("http://rdf.bonsai.uno/flowobject/exiobase3_3_17/")

    g = Graph()
    g.bind('bont', 'http://ontology.bonsai.uno/core#')
    g.bind('brdfat', 'http://rdf.bonsai.uno/activitytype/exiobase3_3_17/')
    g.bind("dc", DC)

    for name, code in data:
        node = URIRef(nat[code])
        g.add( (node, RDF.type, nb.ActivityType) )
        g.add( (node, RDFS.label, Literal(name)) )

    create_dir(output_base_dir / "activitytype" / "exiobase3_3_17")
    with open(
            output_base_dir / "activitytype" / "exiobase3_3_17" / "exiobase3_3_17.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')

    # # TODO: Need to add preferred unit

    df = pandas.read_excel(
        data_dir / "exiobase_classifications_v_3_3_17.xlsx",
        sheet_name="Products_HSUTs",
        header=0
    )
    data = set(zip(df['Product name'], df['product code 2']))

    g = Graph()
    g.bind('bont', 'http://ontology.bonsai.uno/core#')
    g.bind('brdffo', "http://rdf.bonsai.uno/flowobject/exiobase3_3_17/")
    g.bind("dc", DC)

    for name, code in data:
        node = URIRef(nfo[code])
        g.add( (node, RDF.type, nb.FlowObject) )
        g.add( (node, RDFS.label, Literal(name)) )

    create_dir(output_base_dir / "flowobject" / "exiobase3_3_17")
    with open(
            output_base_dir / "flowobject" / "exiobase3_3_17" / "exiobase3_3_17.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')

    # Exiobase locations are hardcoded to geoname URIs, so just use CSV
    # created by hand
    df = pandas.read_csv(
        data_dir / "exiobase_location_uris.csv",
        header=0
    )
    data = set(zip(df['CountryCode'], df['URI']))

    g = Graph()
    g.bind('bont', 'http://ontology.bonsai.uno/core#')
    g.bind('gn', 'http://sws.geonames.org/3202326')
    g.bind('brdflo', "http://rdf.bonsai.uno/location/exiobase3_3_17/")
    g.bind("dc", DC)
    g.bind("schema", "http://schema.org/")

    for name, code in data:
        node = URIRef("http://" + code)
        g.add( (node, RDF.type, URIRef("http://schema.org/Place")) )
        g.add( (node, RDFS.label, Literal(name)) )

    create_dir(output_base_dir / "location" / "exiobase3_3_17")
    with open(
            output_base_dir / "location" / "exiobase3_3_17" / "exiobase3_3_17.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')
