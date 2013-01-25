import sys

sennafile="/home/kimia/srl/python/SemanticRoleMiner/testCases/test2/sennaoutput.txt"
stanfile="/home/kimia/srl/python/SemanticRoleMiner/testCases/test2/stanoutput.txt"
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

#----------------------------------------
def verbLinks(vbn,deplist):
	vlist=[]
	vlist.append(vbn)
	for item in vlist:
		#print "from vlist : ",item
		for dep in allDeps:
			#print "checking dep: ",dep
			if item in dep:
				tok1=dep[0]
				tok2=dep[1]
				if (tok1 in VBNs and tok1!=vbn) or (tok2 in VBNs and tok2 !=vbn):
					skip=1
				else:
					tok1=dep[0]
					tok2=dep[1]
					if tok1 in vlist and tok2 not in vlist:
						vlist.append(tok2)
					elif tok2 in vlist and tok1 not in vlist:
						vlist.append(tok1)
	return vlist
#-----------------------------------------
def scanVerb(sen,vlist):
	banlist=['by','from','and','in',',','of','with']
	sen=sen.replace(","," , ") # should give the same sentence to stanford
	sen=sen.replace(".","")
	sen=sen.replace("  "," ")
	senlist= list(sen.split(" "))
	newsenlist=[]
	newsen=""
	#print vlist
	for i in range(0,len(senlist)):
		#print item,senlist.index(item)+1
		item=senlist[i]
		index=i
		item=item+"-"+str(index+1)
		newsenlist.append(item)

	print "sentence list: ", newsenlist #now i have the whole sentence in form of a list
	for item in newsenlist: 
		index=newsenlist.index(item)
		if item in vlist:
			#print item.split("-")[0]
			newsen+=str(item.split("-")[0])+" "
		elif item.split("-")[0] in banlist:
			if (index>0 and index<len(newsenlist)): #checking if preposition is between 2 related words
				if( newsenlist[index-1] in vlist and newsenlist[index+1] in vlist): 
					#print item.split("-")[0]
					newsen+=str(item.split("-")[0])+" "
			if (index==0 or index==len(newsenlist)): #checking if preposition is before related words in the beginning or in the end
				if( newsenlist[index-1] in vlist or newsenlist[index+1] in vlist): 
					print item.split("-")[0]
					newsen+=str(item.split("-")[0])+" "
				
	print newsen+" ."

#-----------------------------------------
Senna=modifySenna(sennafile)
VBNs=[]
Preps={}
for sen,val in Senna.items():
	for num,token in val.items():
		for a,b in token.items():
			if b[1]=="VBN":
				VBNs.append(a)

#print VBNs

Stan=modifyStanf(stanfile)
for key,val in Stan.items():
    for i, prep in val.items():
        pred=prep.keys()[0]
        rel=prep.values()[0]
        token1=rel[0]
        token2=rel[1]
        if token1 in VBNs:
           Preps[token1]=(pred,token2)
        elif token2 in VBNs:
           Preps[token2]=(pred,token1)
	
#print Preps



i=0
vals=Stan.values()[0]
temp=vals.values()  
allDeps=[] #all relations in one list
newlist=[]
for v in temp:
    #print v.keys()[0]
    #print v.values()[0]
	a=(v.values()[0][0],v.values()[0][1])
	if a not in allDeps:
		allDeps.append(a)





#newlist=[]
#allDeps=[("a","b"),("b","c"),("d","e"),("g","e"),("b","d"),("t","n"),("n","p")] 
#allDeps2=[("testing-2","Laboratory-1"),("isolated-18","testing-2"),("testing-2","conducted-3"),("laboratories-8","state-5"),("laboratories-8","public-6"),("laboratories-8","health-7"),("conducted-3","laboratories-8"),("conducted-3","Connecticut-10"),("conducted-3","Maryland-12"),("Connecticut-10","Maryland-12"),("conducted-3","Pennsylvania-14"),("Connecticut-10","Pennsylvania-14"),("conducted-3","Wisconsin-16"),("Connecticut-10","Wisconsin-16"),("isolated-18","has-17"),("ROOT-0","isolated-18"),("isolated-18","salmonellae-19"),("isolated-18","53-21"),("samples-24","55-23"),("53-21","samples-24"),("samples-24","taken-25"),("packages-28","intact-27"),("taken-25","packages-28"),("scrape-34","frozen-30"),("scrape-34","yellow-31"),("scrape-34","fin-32"),("scrape-34","tuna-33"),("packages-28","scrape-34"),("taken-25","sushi-36"),("sushi-36","prepared-37"),("product-43","the-39"),("product-43","implicated-40"),("product-43","scrape-41"),("product-43","tuna-42"),("prepared-37","product-43")]

#testcase 1
#sentence="a total of 316 individuals infected with the outbreak strains of SalmonellaBareilly or SalmonellaNchanga have been reported from 26 states and the District of Columbia."
#testcase 2
sentence="workers on a gas production platform in the Bass Strait want their barge returned to port after a major outbreak of salmonella and gastroenteritis."
#testcase 3
#sentence="in total, 36 of more than 200 workers have fallen ill in the 2 weeks since the outbreak, their union said."
#testcase4
#sentence="laboratory testing conducted by state public health laboratories in Connecticut, Maryland, Pennsylvania and Wisconsin has isolated salmonellae from 53 of 55 samples taken from intact packages of frozen yellow fin tuna scrape from sushi prepared with the implicated scrape tuna product."


newlist=list(allDeps)

#vlist=["taken-25"]
#mining new approach
for vbn in VBNs:
	print vbn
	vlist=verbLinks(vbn,allDeps)
	if len(vlist)>1:
		sen=scanVerb(sentence,vlist)
	



