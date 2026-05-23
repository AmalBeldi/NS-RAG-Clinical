from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF,RDFS
import re
NS=Namespace('http://example.org/nsrag/')
def safe_uri(s): return re.sub(r'[^a-zA-Z0-9_]+','_',str(s)).strip('_')
def nx_to_rdf(nxg):
    rdf=Graph(); rdf.bind('nsrag',NS)
    for n,a in nxg.nodes(data=True):
        s=NS[safe_uri(n)]; rdf.add((s,RDF.type,NS[safe_uri(a.get('type','Entity'))])); rdf.add((s,RDFS.label,Literal(a.get('label',n))))
        for k,v in a.items():
            if k not in {'type','label'}: rdf.add((s,NS[safe_uri(k)],Literal(v)))
    for u,v,d in nxg.edges(data=True): rdf.add((NS[safe_uri(u)],NS[safe_uri(d.get('relation','relatedTo'))],NS[safe_uri(v)]))
    return rdf
def rdf_triples_count(rdf): return len(rdf)
