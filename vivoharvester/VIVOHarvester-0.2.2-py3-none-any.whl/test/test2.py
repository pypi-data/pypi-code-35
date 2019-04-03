import rdflib
from rdflib import Graph


g = Graph()
g.parse("https://s3.amazonaws.com/vivouploads/rdf/users/1003.rdf",
        format="xml")

s = g.serialize(format='nt')
# g.serialize("test.nt", format="nt")

print(s)
