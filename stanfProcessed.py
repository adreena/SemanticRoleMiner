def modifyStanf(inputFile):

	sentences_Stanf={}
	i=-1
        dummyfile=open(inputFile,'r')
	stanfIterator=dummyfile.read()
	#separating sentences by iterator
	for line in stanfIterator.split("\n"):
	    
	   #First
	   #sentence detected , create a key in sentences dictionary
	    if line=="(ROOT":	 
		i+=1        
		sentences_Stanf['sen'+str(i)]={}
	   #Second 
	   #finding root and its index of each sentences detected    
	    if line[0:4]=="root":
	       root=line.replace(",","")
	       root=root.replace("("," ")
	       root=root.replace("-"," ") 
	       root=root.replace(")","")
	       root=root.split(" ")
	       index=root[-1]
	       root=root[-2]
	       sentences_Stanf["sen"+str(i)]["root"]=(index,root)

	return sentences_Stanf   
        #Third , now root detected 
	   #going to sennaIterator to find target column
	#output of stanford 
	#2 sentences are identified sentences_Stan={'sen2': {'root': 'sanitized'}, 'sen1': {'root': 'have'}}
	#for each a root is found       

