def makeGephi(St,inputFile):
   output=open("/home/kimia/"+inputFile+"/gephi.dot","w")
   output.write("digraph sample {\n")
   for key,val in St.items():
       #print key,val
       tokens=val.split(" ")
       node1=tokens[0]
       edge=tokens[1]
       node2=tokens[2]
       print node1,edge,node2
       output.write("\""+node1+"\""+" -> "+"\""+node2+"\" "+"[ label = \""+str(edge)+"\" ];\n") 
   output.write("}")
   output.close()
