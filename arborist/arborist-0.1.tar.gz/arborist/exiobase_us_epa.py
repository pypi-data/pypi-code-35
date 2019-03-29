"""Generate the URIs needed for correspond EXIOBASE to US EPA elementary flow list.
This code creates both `flowObjects`.
As these are not present in any online data, we have hard coded our own URIs"""

from . import data_dir
from .filesystem import create_dir
from pathlib import Path
import pandas

DOCKER = """Run the following to convert to JSON-LD:
    cd {}
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out JSON-LD flowobject/exiobase3_3_17/exiobase3_3_17.ttl > flowobject/exiobase3_3_17/exiobase3_3_17.jsonld
"""

def generate_exiobase_us_epa_uris(output_base_dir):
    data = pandas.read_csv(data_dir / 'exiobase_to_usepa_ghg.csv')
    output_base_dir = Path(output_base_dir)
    
    output_dir = create_dir(output_base_dir / "flowobject" / "exiobase3_3_17")
    
    with open(output_dir / "exiobase3_3_17.ttl", "w") as f:
    
        f.write('@prefix bont: <http://ontology.bonsai.uno/core#> .\n')
        f.write('@prefix dc: <http://purl.org/dc/terms/> .\n')
        f.write('@prefix ns0: <http://purl.org/vocab/vann/> .\n')
        f.write('@prefix cc: <http://creativecommons.org/ns#> .\n')
        f.write('@prefix owl: <http://www.w3.org/2002/07/owl#> .\n')
        f.write('@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n')
        f.write('@prefix foaf: <http://xmlns.com/foaf/0.1/> .\n')
        f.write('@prefix dtype: <http://purl.org/dc/dcmitype/> .\n')
        f.write('@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n')
        f.write('@prefix brdclass: <http://rdf.bonsai.uno/flowobject/exiobase3_3_17/> .\n')
        f.write('@prefix brdf: <http://rdf.bonsai.uno/flowobject/exiobase3_3_17/> .\n')
        f.write('@prefix chemrdf: <http://www.chemspider.com/> .\n')
        f.write('@prefix chemrdf: <http://www.chemspider.com/> .\n')
        f.write(' \n')
        
        f.write('<http://rdf.bonsai.uno/flowobject/exiobase3_3_17/>\n')
        f.write('  a dtype:Dataset ;\n')
        f.write('  dc:title "The correspondence between EXIOBASE emissions with US EPA Chemicals as Flow Objects"@en ;\n')
        f.write('  dc:description "The correspondence between EXIOBASE emissions with US EPA Chemicals as Flow Objects"@en ;\n')
        f.write('  foaf:homepage <http://rdf.bonsai.uno/fflowobject/exiobase3_3_17//documentation.html> ;\n')
        f.write('  ns0:preferredNamespaceUri "http://rdf.bonsai.uno/flowobject/exiobase3_3_17/#" ;\n')
        f.write('  owl:versionInfo "Version 0.1 - 2019-03-25"@en ;\n')
        f.write('  dc:modified "2019-03-25"^^xsd:date ;\n')
        f.write('  dc:publisher "bonsai.uno" ;\n')
        f.write('  dc:creator <http://bonsai.uno/foaf/bonsai.rdf#bonsai> ;\n')
        f.write('  dc:contributor "Tiago Morais";\n')
        f.write('  cc:license <http://creativecommons.org/licenses/by/3.0/> ;\n')
        f.write('  rdfs:comment """First ever version 0.1 :\n')
        f.write('                  Will change!\n')
        f.write('               """@en .\n')
        f.write(' \n')         
        
        
        for i in range(0,len(data)):
            name = data['US_EPA'].values[i]
            
            if pandas.notnull(name):
                code = data['URI'].values[i]
                sp = code.split('/')
                code_in = sp[5]
                f.write('brdf:' + code_in + ' a bont:FlowObject ;\n')
                f.write(' owl:sameAs chemrdf:' + code_in + '.rdf ;\n')
                
                if data['Count_in_USE_EPA'].values[i] > 1:
                    code = data['URI_classes'].values[i]
                    sp = code.split('/')
                    code_in = sp[5]
                    f.write(' rdfs:subClassOf brdclass:'+ code_in +' ;\n')
                
                f.write(' rdfs:label "'+data['US_EPA'].values[i]+'" .\n')
                f.write('  \n')
    
    print(DOCKER.format(output_base_dir))
