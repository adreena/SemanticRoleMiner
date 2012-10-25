#Goal : For each sentence args for a root are investigated


def findPreds(senna):
    elementID=senna.values()
    for i in elementID:
        token=i.keys()
        cols=i.values()
	cols=cols[0]
        #print cols
        tok_keys=cols.keys()
        tok_tags=cols.values()
        for col, tag in cols.items():
            if tag[-1]=="V":
	       print tag , col 


def findDomain(args):

    elements= args.keys()
    domains={}
    for label in elements:
        first=args[label][0][1]       
	#print args[label][0]    #first token with this label 
	last=args[label][-1][1]
        #print args[label][-1]   #last token with this label
        domains[label]=(first,last)
    return domains    
   


def findArg((index,root),targetDict):
    
     tokenLabels={}
     Labels={}
    #---Testing function arguments Perfect working
     #print index
     #print root
     #print targetDict

     #--Finding the target column for retreiving correct args
     #--going through root element to find where predicate has happened its column is marked as 'V'
     #--I take all elements of root row and check for detection of V 
     #--to mark its id as target column

     targetColumn='Null'
     for element_id in targetDict[int(index)][root]:
         #print element_id
         #print targetDict[int(index)][root][element_id]
         take=targetDict[int(index)][root][element_id]
         #print take
         #print take[-1] trying to find V in S-V as verb
         if take[-1]=="V":
            #print element_id
            targetColumn=element_id
     #print targetColumn
     #sanityCheck of right column Id 
     #print targetDict[int(index)][root]
     #tok=targetDict[1]
     #print tok
     #for key in tok:
     #   print tok[key][targetColumn]
     

     # having all args for all tokens  
     for key in targetDict:
         token=targetDict[key]
         #print token
         #--token is now a dictionary 
         #print key #--token location in the sentence
         #print "**"+str(key)
         for word in token:
            #print targetDict[key][word][targetColumn] # This the target Column or Label for each column
            modify=targetDict[key][word][targetColumn]
            if modify!="O":
		    temp=modify.split('-')
		    #print temp[0] for begining and ending
		    #print temp[1]
                    myArg=temp[1]+"-"+root
		    #print word 
		    #tokenLabels[word]=temp[1]
		    if myArg in tokenLabels:
		       tokenLabels[myArg].append((word,key))
		    else:
		       tokenLabels[myArg]=[]
		       tokenLabels[myArg].append((word,key)) 
          
     #tokenLabels['Tanks']='A0'
     return tokenLabels

#-------------------------------------------------------------------------------------------

def findParts(targetTuple,AR,root):
    newAR=""
    #print "targettuple"+str(targetTuple)
    dep=targetTuple[0]
    part1=targetTuple[1]
    #print "dep"+str(dep)
    sw1=0
    sw2=0
    part2=targetTuple[2]
    #print part1, part2
    #print AR
    verbconnection=0
    for arg in AR:
       newAR=""
       
       for tup in AR[arg]:
          
           if tup[0]==part1[0] and str(tup[1])==part1[1]: #finding first match
               sw1=1 
               #print arg, arg[0]
               #print tup[0]
	       if arg[0]=="V":
                  verbconnection=1
                  #print "1"
                  #print "hi"
		  #newAR="V-"+str(root)
           elif tup[0]==part2[0] and str(tup[1])==part2[1]: #finding second match
               sw2=1
               #print  arg, arg[0]
               #print tup[0]
               if arg[0]=="V":
                  verbconnection=1
                  #print "1"
		  #newAR="V-"str(root)
           if sw1==1 and sw2==1:
	       break # good point to break out of loop as the first matching case is found

       if sw1==1 and sw2==1 : # means 2 parts are found
           #print arg, part1, part2       #             A1   ['debris', '11'] ['contamination', '17']
           #print dep, arg, part1 , part2 #  conj_and   A1   ['debris', '11'] ['contamination', '17']
           #print verbconnection  
	   if verbconnection==1: 
               newAR="Link-"+str(root)
           else :
               newAR=arg
           #print part1
	  
	   break
    return newAR

def mixDepArg(ST,AR):
     mixDict={}
     temp=[]
     root=ST["root"]
     root=root[1]
     #print root
     for ids in ST:
       if ids!="root":
         #print ids
         items= ST[ids] 
         #print items  #amod(debris-11, visible-10)
         items=items.replace("(", ",")
         items=items.replace(")", " ")
	 items=items.replace(" ", "")
         #print items
         temp=items.split(",")
         #print temp  #['amod','debris-11','visible-10']
         #print temp[0]
         #print temp[1]
         temp[1]= temp[1].split("-") #spliting the word from its location into : temp[1]=debris-11 becomes =>temp[1][0]=debris temp[1][1]=11
         #print temp[1]
         temp[2]= temp[2].split("-") 
         #print temp  #['amod', ['debris', '11'], ['visible', '10']]
         #print temp
         newAR=findParts(temp, AR,root)
         #print newAr
         mixDict[ids]={}
         if newAR!="":
         	mixDict[ids][newAR]={}
         	mixDict[ids][newAR][temp[0]]=[temp[1],temp[2]]
 
         #print "----"
        
     if mixDict!="Null":
        return mixDict       


