import rdflib
from rdflib.graph import Graph
from rdflib import plugin
from rdflib.namespace import Namespace


def findDisease(diseaseList,args,mixArgs):
    
    k,v=args.items()
    
    for item in v:
        key=item.keys()
        val=item.values()
             

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

def makeTurtle(graph,inputFile):
    f=open("/home/kimia/"+inputFile+'/temp.ttl','w') 
    s=graph.serialize(format="turtle")
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

    #--- generate ttl format from nt
    makeTurtle(graph,inputFile)

 
    #query
#    graph.parse("/home/kimia/"+inputFile+'/temp.ttl',format='turtle')
#    plugin.register('sparql', rdflib.query.Processor,'rdfextras.sparql.processor', 'Processor')
#    plugin.register('sparql', rdflib.query.Result,'rdfextras.sparql.query', 'SPARQLQueryResult')
#    rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
#    ns1=Namespace("http://")

    #--------- testing 1: find all A1 statements
#    qres = graph.query("""SELECT ?a ?b
#                             WHERE {
#          			?a ns1:A1 ?b .
#     				  }""",initNs=dict(ns1=Namespace("http://"))) 
    #for row in qres.result:  
      #print "ns1:A2"
      #print("%s ns1:A1 %s"%row)     

    #--------- testing 2: find all salemonella statements
#    qres = graph.query("""SELECT ?s ?p ?pred ?obj
#                             WHERE {
#                                ?s ?p ns1:outbreak-19.
#          		        ns1:outbreak-19 ?per ?obj.
#     				  }""",initNs=dict(ns1=Namespace("http://"))) 
    #for row in qres.result:  
      #print "ns1:A2"
      #print("%s  %s  %s  %s"%row) 

    #--------- testing 3: searching for string=""
#    qres = graph.query("""SELECT *
#                             WHERE {
#                                 {?s ?p ?o;
#				  FILTER(regex(?o,"outbreak","i"))    
#				  }
#				UNION
#                                  {?s ?p ?o;
#				   FILTER(regex(?s,"outbreak","i"))
#                                   UNION {SELECT ?s1 ?p1 ?o1 WHERE {?s1=?o}
#                                   }
#     				  }""") 
#
#    for row in qres.result:  
#      print("%s %s %s"%row)   

