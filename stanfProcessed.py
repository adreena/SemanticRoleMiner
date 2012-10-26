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
               counter=0        
	       sentences_Stanf['sen'+str(i)]={}
	   #Second 
	   #finding root and its index of each sentences detected    

            elif line== "" or line[0]==" " :
               line=""
               #do nothing
            else :
               #print line
               line=line.replace(",","")
               line=line.replace("("," ")
               line=line.replace(")","")
               line=line.split(" ")
               #print line[0], line[1], line[2]
               sentences_Stanf["sen"+str(i)][counter]={}
	       sentences_Stanf["sen"+str(i)][counter][line[0]]=[]
               sentences_Stanf["sen"+str(i)][counter][line[0]].append(line[1])
	       sentences_Stanf["sen"+str(i)][counter][line[0]].append(line[2])   	
               counter+=1

	return sentences_Stanf   
        #Third , now root detected 
	   #going to sennaIterator to find target column
	#output of stanford 
	#2 sentences are identified sentences_Stan={'sen2': {'root': 'sanitized'}, 'sen1': {'root': 'have'}}
	#for each a root is found
        # new version of out put:
	#{'sen0': {0: 'nsubj(have-8, Tanks-1)', 1: 'partmod(Tanks-1, used-2)', 2: 'prep_for(used-2, storage-4)', 3: 'nn(waters-7, process-6)', 4: ..}}


       

