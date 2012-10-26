#preprocessing senna file
def modifySenna(inputFile):
         
	j=0
        #print inputFile			   
	dummyfile=open(inputFile,'r')
	sennaIterator=dummyfile.read()
        sentences_Senna={}
        tokenloc=0
	sentences_Senna["sen0"]={}
	for line in sennaIterator.split("\n"):
           if line!="":           
		   #print line
		   tokens=line.replace(" ","")
		   tokens=tokens.replace("\t","|")
		   tokens=tokens.split("|")
		   #print tokens
		   tokenloc+=1
		   if tokens[0]!=".": 
			counter=1
			sentences_Senna["sen"+str(j)][tokenloc]={}
		        sentences_Senna["sen"+str(j)][tokenloc][str(tokens[0])+"-"+str(tokenloc)]={}
			for element in tokens[1:]:
			    #print element +"---"
			    sentences_Senna["sen"+str(j)][tokenloc][str(tokens[0])+"-"+str(tokenloc)][counter]=element

			    counter+=1
		   else: 
		     j+=1 
		     #print "end"
		     tokenloc=0
		     sentences_Senna["sen"+str(j)]={}

        return sentences_Senna

