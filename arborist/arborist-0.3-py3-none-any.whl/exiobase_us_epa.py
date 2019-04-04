"""Generate the URIs needed for correspond EXIOBASE to US EPA elementary flow list.
This code creates both `flowObjects`.
As these are not present in any online data, we have hard coded our own URIs"""

from .filesystem import create_dir
from . import data_dir
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS, OWL
import pandas


def generate_exiobase_us_epa_uris(output_base_dir):
    data = pandas.read_csv(data_dir / 'exiobase_to_usepa_ghg.csv')
    output_base_dir = Path(output_base_dir)

    nb = Namespace("http://ontology.bonsai.uno/core#")

    g = Graph()
    g.bind('bont', 'http://ontology.bonsai.uno/core#')
    g.bind('brdfusepa', 'http://rdf.bonsai.uno/flowobject/us_epa/')
    g.bind('brdfusepaexiobase', 'http://rdf.bonsai.uno/flowobject/exiobase3_3_17/')
    g.bind("dc", DC)
    g.bind("owl", OWL)

    for i in range(0,len(data)):
            name = data['US_EPA'].values[i]

            if pandas.notnull(name):
                code = data['URI'].values[i]
                sp = code.split('/')
                code_in = sp[5]

                nme = code_in+'.rdf'

                node = URIRef("brdfusepa:{}".format(code_in))

                g.add((node, RDF.type, nb.FlowObject))
                g.add((node, OWL.sameAs, URIRef("hhttp://www.chemspider.com/{}".format(nme))))
                g.add((node, RDFS.label, Literal(name)))
                g.add((node, DC.title, Literal("US EPA Elementary Flow List correspondence with EXIOBASE 3.3.17")))
                g.add((node, DC.description, Literal("US EPA Elementary Flow List correspondence with EXIOBASE 3.3.17")))
                g.add((node, DC.publisher, Literal("bonsai.uno")))
                g.add((node, DC.creator, URIRef("http://bonsai.uno/foaf/bonsai.rdf#bonsai")))
                g.add((node, DC.contributor, Literal("Tiago Morais")))
                g.add((node, URIRef("http://creativecommons.org/ns#license"), URIRef('http://creativecommons.org/licenses/by/3.0/')))


                if data['Count_in_USE_EPA'].values[i] > 1:
                    code = data['URI_classes'].values[i]
                    sp = code.split('/')
                    code_in = sp[5]

                    group = URIRef("brdfexiobaseclass:{}".format(code_in))

                    g.add((node, RDFS.subClassOf, group))


    create_dir(output_base_dir / "flowobject" / "exiobase3_3_17")
    with open(
            output_base_dir / "flowobject" / "exiobase3_3_17" / "exiobase3_3_17.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')


