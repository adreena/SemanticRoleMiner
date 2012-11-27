import rdflib
from rdflib.graph import Graph
from rdflib import plugin
from rdflib.namespace import Namespace


def makeNT(statement,inputFile):
    f=open("/home/kimia/"+inputFile+'/temp.nt','w')
    for val in statement.values():
        #f.write("< "+ val+" >.\n")
        tokens=val.split(" ")
        f.write("<http://"+tokens[0]+"> <http://"+tokens[1]+"> <http://"+tokens[2]+"> .\n")

def makeRDFXML(graph,inputFile):
    f=open("/home/kimia/"+inputFile+'/temp.rdf','w') 
    s=graph.serialize(format="xml")
    for line in s.split("\n"):
        f.write(line+"\n")

  
def makeGraph(statement,inputFile):	
    
    #--- generate ntriple format
    makeNT(statement,inputFile)
 
    #--- make a graph from nt
    graph=Graph()
    graph.parse("/home/kimia/"+inputFile+"/temp.nt",format='nt')

    #--- generate RDF/XML format from nt
    makeRDFXML(graph,inputFile)

 
    #query
    graph.parse("/home/kimia/"+inputFile+'/temp.rdf',format='xml')
    plugin.register('sparql', rdflib.query.Processor,'rdfextras.sparql.processor', 'Processor')
    plugin.register('sparql', rdflib.query.Result,'rdfextras.sparql.query', 'SPARQLQueryResult')
    rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    
    qres = graph.query("""SELECT ?a ?b
                             WHERE {
          			?a ns1:A1 ?b .
     				  }""",initNs=dict(ns1=Namespace("http://"))) 
    for row in qres.result:
      print("%s A1-relation %s" % row)     
    

