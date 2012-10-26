#Goal : For each sentence args for a root are investigated


def findPreds(senna):
    preds={}
    #print senna
    #print senna.keys()

    for sennaKey,sennaVal in senna.items():
        token=sennaVal.keys()
        cols=sennaVal.values()
	cols=cols[0]
        #print cols
        tok_keys=cols.keys()
        tok_tags=cols.values()
        for col, tag in cols.items():
            if tag[-1]=="V" :
               #a=[]
               #a.append(token)
               
	       #print tag , col, token[0]
               #print root, rootID 

	       token.append(str(sennaKey))
               preds[str(col)]=token
    return preds
#-----------------------------------------------------------------

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
   
#------------------------------------------------------------------

def findArg(verb,targetDict):
    
     tokenLabels={}
     Labels={}
    #---Testing function arguments Perfect working
     #print verb
     #print targetDict
     root=verb.split("-")
     index=root[1]
     root=root[0]
     

     #--Finding the target column for retreiving correct args
     targetColumn='Null'
     for element_id in targetDict[int(index)][str(verb)]:
         #print element_id
         #print targetDict[int(index)]["reported-17"][element_id]
         take=targetDict[int(index)][str(verb)][element_id]   
         if take[-1]=="V":
            #print element_id
            targetColumn=element_id
     

     #--having all args for all tokens  
     for item in targetDict.values():
         val=item.values()
         token=item.keys()
         #print token
	 val=val[0]
         arg=val[targetColumn]
	 if arg!="O":
	 	arg=arg.split("-")
         	arg=arg[1]
                myArg=arg+"-"+root
		#print myArg 
		if myArg in tokenLabels:
		   tokenLabels[myArg].append(token)
		else:
		   tokenLabels[myArg]=[]
		   tokenLabels[myArg].append(token) 
          
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


