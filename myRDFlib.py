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
    
        
    

