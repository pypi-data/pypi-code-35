"""Generate the URIs needed for core activity type `electricity grid`.
Handcrafted as not available elsewhere."""

from . import data_dir
from .filesystem import create_dir
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS
import pandas


def generate_electricity_grid_uris(output_base_dir):
    output_base_dir = Path(output_base_dir)

    nat = Namespace("http://rdf.bonsai.uno/activitytype/core/")
    nb = Namespace("http://ontology.bonsai.uno/core#")

    g = Graph()
    g.bind('bont', 'http://ontology.bonsai.uno/core#')
    g.bind('brdfat', 'http://rdf.bonsai.uno/activitytype/core/electricity_grid/')
    g.bind("dc", DC)

    node = URIRef("http://rdf.bonsai.uno/activitytype/core/eg")
    g.add( (node, RDF.type, nb.ActivityType) )
    g.add( (node, RDFS.label, Literal("Electricity grid")) )
    g.add( (node, DC.title, Literal("Electricity grid")) )
    g.add( (node, DC.description, Literal("Electricity grid activity type")) )
    g.add( (node, DC.publisher, Literal("bonsai.uno")) )
    g.add( (node, DC.creator, URIRef("http://bonsai.uno/foaf/bonsai.rdf#bonsai")) )
    g.add( (node, DC.contributor, Literal("Tiago Morais")) )
    g.add( (node, URIRef("http://creativecommons.org/ns#license"), URIRef('http://creativecommons.org/licenses/by/3.0/')) )

    create_dir(output_base_dir / "activitytype" / "core" / "electricity_grid")
    with open(
            output_base_dir / "activitytype" / "core" / "electricity_grid" / "electricity_grid.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')
