

#triples_file=open("~/srl")
def s_P_o(token2,rel,token1):
    
    print str(token2)+rel+str(token1)



def mainArg(token,mixedArgs):
    elements=mixedArgs.values()
    for temp in elements:
        if len(temp)!=0:
	   arg=temp.keys()[0]
           value=temp.values()
	   value=value[0]
           #print value 
           value=value.values()
           #print value[0][0]
           if token in value[0] and arg!="V":
              print (token,"is",arg)
              break
           
           #if part1==token or part2==token:
              #print token, arg
    print "----"



#-- Check if verb is negate or not
def checkNegate(verb,mixedArgs):
     elements = mixedArgs.values()
     neg=""
     #print elements
     #print "---"
     for temp in elements:
        if len(temp)!=0 and temp.keys()[0]=="V":
          value=temp.values()
          #print value[0].keys()
          if value[0].keys()[0]=="neg":
              neg="not"
              break
    # print arg
     return neg
     #print "----------------"

#-- Find direct Object for a given verb. these types of verbs usually have nsubj
def findObj(verb,mixedArgs):
    obj=[]
    elements= mixedArgs.values()
    for temp in elements:
        if len(temp)!=0 :
	   value=temp.values()
           value=value[0]           
           rel=value.keys()
           #print rel
           value=value.values()
           if verb in value[0] and rel[0]=="dobj":
              obj.append(value[0][1])
              
    return obj          



#-- I first extracted arg, rel, token1 and token2

def makeRel(mixedArgs):
    for elements in mixedArgs.values():
      #print elements #returns a dict
      negate=" " # this is my negate switch to recog verb 
      arg=elements.keys()
      #print arg
      if len(arg)!=0:
         arg=arg[0]
         elements=elements[arg] # returns a list of dependency rel
         #print rel
         rel=elements.keys()
         rel=rel[0]
         #print rel   #relation retirieved
         elements=elements[rel] #a tuple of 2 tokens
         token1=elements[0]
         token2=elements[1]
         #print token1 #each token along with their location
         #print token2 
 
         if arg=="V":
		#-- token1 is verb ; hence should be checked if it's negative or positive
		negate= checkNegate(token1,mixedArgs)
		if rel=="nsubjpass": #this relation makes token2 as main nsubject     
		 	s_P_o(token2,"is"+negate,token1)
			mainArg(token2,mixedArgs)
                elif rel=="nsubj":  #this relation takes verb as the name of relation and I need to search for object of the verb
                        obj=findObj(token1,mixedArgs)
                        for item in obj:
			   s_P_o(token2,str(negate)+str(token1),item)
                           mainArg(item,mixedArgs)
                        mainArg(token2,mixedArgs)
                        
         elif rel=="nn" or rel=="amod":
                s_P_o(token1,"is",token2)

         




         
