import sys
from StanSennaClass import SenSta
import os
from nltk.corpus import propbank
from sennaProcessed import modifySenna
from stanfProcessed import modifyStanf
import en #for converting verbs into present tense
from stemming.porter2 import stem # for removing ing,ial ,...
from en import numeral
import en
import re
import rdflib
from rdflib.graph import Graph
from rdflib import plugin
from rdflib.namespace import Namespace

from Visualizer import makeGephi
#excluded "nn":"--","amod":"is"
dictionary={"dep":"--","abbrev":"sameAs","acomp":"is","advmod":"more-detail","agent":"by","appos":"or","attr":"","csubjpass":"more-detail","dobj":"direct-object","iobj":"to","neg":"not","nsubj":"subject","csubj":"subject", "nsubjpass":"subject","num":"number", "number":"currency","partmod":"moreDetail", "poss":"possession", "prep_on":"on","prep_in":"in","prep_by":"by","prep_since":"since", "prep_with":"with", "prep_at":"at","prep_after":"after","prep_for":"for",'prep_behind':'behind',"prep_of":"of","prep_to":"to","prep_from":"from" , "prep_among":"among","prep_without":"without" ,"quantmode":"quantity", "tmod":"time"}
banlist=['behind','without','among','estimated','is','are','and','an','a','for','the','by','from','and','in',',','of','with','on','at','under','to','after',"or","beyond","and","becasue","instead","such","addition","due","all","rather","well"]

path="/home/kimia/srl/"

#------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------------
#--- Finding all the tokens directly connected to verb, input is all tokens and Stanford parser output which cotains dependecies. output is rellist conatining all related tokens to verb.
#------------------------------------------------------------------
def verbRelatives(vlist,Stan,indices): #works based on dependecies discovered by stanford
	rellist=[]
	verb=vlist[0]
	print "Stan",Stan
	#print "verb to rel : ",verb
	for item in Stan:
		tok1=item.values()[0][0]
		tok2=item.values()[0][1]
		print "tok1-tok2 in rellist ",tok1,tok2
		print indices
		if tok1.split("-")[0:-1][0]==verb.split("-")[0:-1][0] and tok2!= 'ROOT-0':
			#rem=tok2.split("-")[-1] #index of indices
			#tok2=indices[int(rem)+1]
			rellist.append(tok2)
			#print "tok2:",tok2
		elif tok2.split("-")[0:-1][0]==verb.split("-")[0:-1][0] and tok1!='ROOT-0':
			#rem=tok1.split("-")[-1] #index of indices
			#tok1=indices[int(rem)-1]
			#print "tok1:",tok1
			rellist.append(tok1)

	#print rellist #number tags are fixed based on the real sentence
	return rellist
#------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------------
#---- rolFinder gets the verb , makes it present tense using en library, and then by using propBank library finds all roles of the verb version.01. because senna doesn't provide the version of the verb ! I am assuming one 01 at the end of each verb. Output returns a dictionary of {"A0":"", "A1":""...}
#------------------------------------------------------------------
def roleFinder(verb):
	#--converting verb into its present tense
	print "verb**",verb
	
	if verb=="find" or verb=="found" : tverb="find"
	else: tverb=en.verb.present(verb)
	print "targetverb **** ",tverb	
	if tverb=="emerge": propVerb=tverb+".02"
	else: propVerb=tverb+".01"
	print propVerb
	if propVerb=="re-cover.01": propVerb="recover.01"
	allroles={}
	if propVerb=="vaccinate.01": 
		allroles={'A0':'Vaccinator','A1':'Vaccinated','A2':'Against_what/disease'}
	
	else:
		roles=propbank.roleset(propVerb)
		for role in roles.findall('roles/role'):
			role.attrib['descr']=role.attrib['descr'].replace(" ","-")
			allroles["A"+str(role.attrib['n'])]=role.attrib['descr']

	return allroles
#------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------------

#----------------------------------------
#--- translating list of word connected to verb into triples, "vlist" is a list of all tokens in the "result" sentence , in this list the first item is always the verb of the sentence.  
#----------------------------------------
def translateSent(vlist,result,Poss,indices,PrSent):
	STs=[]

	#--- Stanford Translations Dictionary

	#print "to check nmubers: ",vlist #vlist has all tokens involved with their location attached to them

	#--- SenSta class accepts a sentence written in a file format, so for every sentence being sent to translateSent() in "result" argument , the sentence is first saved into a file with base directory mentioned in "inputFile"
	
	#-- 1- writing the sentence in file.
	stanfile=open(path+"SemanticRoleMiner/code/test_input.txt","w")
	stanfile.write(result)
	stanfile.close()
	

	sbj={}
	obj=[]
	i=0
	
	#-- 2- the first verb in vlist is the targetverb which is splited from its location of the main text. verb is set to default value of "not found".
	targetverb=vlist[0].split("-")[0:-1][0]

	
	verb="not found"

	#-- 3- processing stanford-parser and senna on the textfile, the results are store into 2 dictionaries , Stan and Senn
        inputFile="srl/SemanticRoleMiner/code"
	myTestFile=SenSta(inputFile)
	myTestFile.makeSenna()
	myTestFile.makeStanf()
	Stan= myTestFile.stanfDict['sen0'].values()
	Senn= myTestFile.sennaDict['sen0'].values()
	
	
	#thissent=[]
	#thissent=result.split(" ")
	#-- 3.5 finding matches for date-pattern to merge all numbers into just 1 object connected to the target verb
	# sentence is in result string, so i have to find the domain of tokens. I can add the location of any tokens involved into this pattern in 1 list
	months={'January':01,'Jan':"01",'February':"02","Feb":"02","March":"03","Mar":"03","April":"04","Apr":"04","May":"05","June":06,"Jun":"06","July":"07","Jul":07,"August":"08","Aug":"08","September":"09","Sep":"09","October":"10","Oct":"10","November":"11","Nov":11,"December":"12","Dec":"12"}

	#datePatternDomain=[]
	dateObjects={}
	datepattern1=r"(\d{1,2}\s\w+\s\d{1,4})"
	match=re.findall(datepattern1,result)
	
	for item in match: # generalizing dates, number tags fixed
		tempSent=PrSent
		toks=str(item).split(" ")
		rep=item.replace(" ","")
		tempSent=tempSent.replace(item,rep)
		templist=tempSent.split(" ")
		
		index=templist.index(rep)+1
		tok0Ind=index
		tok1Ind=index+1
		tok2Ind=index+2
		#print templist,tok0Ind,tok1Ind,tok2Ind

		if toks[1] in months.keys():
			#print"+++++++", item #toks[0],toks[1],toks[2]
  			newTok=str(toks[0])+"/"+months[toks[1]]+"/"+str(toks[2])
			tok0=toks[0]
			tok0=tok0+"-"+str(tok0Ind)
			tok1=toks[1]
			tok1=tok1+"-"+str(tok1Ind)
			tok2=toks[2]
			tok2=tok2+"-"+str(tok2Ind)

			#print "\n((dates))\n", tok0,tok1,tok2
			#print indices
			
			dateObjects[newTok]=(tok0,tok1,tok2)
	print "dates detected in sentence: ", dateObjects


	#--4  Senna Translation-----------------------------
	#--   4-1 Find roles , calling roleFinder with targetverb, example : targetverb="conducted-2" , allRoles={"A0":"conductor", "A1":".."..}
	allRoles={}	
	allRoles=roleFinder(targetverb) 

	#--  4-2 Finding relatives of a verb, all directly connected tokens are gathered in verbRel.
	verbRel=[]
	#print "**vlist ",vlist
	verbRel=verbRelatives(vlist,Stan,indices)
	#print "*verbRel ",verbRel #fixed

	#-- 4-3 Discovering the arg labels senna has assigned to the tokens, all Args are gathered in roleDep example:[('testing-2', 'A1'), ('laboratories-8', 'A0'),...]
	roleDep=[]
	for item in Senn:#NER
		values=item.values()[0].values() #NER
		#print "values of senna:",values
		if values[2]!="O" and (values[2].split("-")[0]=="B" or values[2].split("-")[0]=="S"):
			tok1=item.keys()[0]
			tok1=indices[int(tok1.split("-")[-1])-1]
			tok2=values[2].split("-")[1:][0]
			#print "**2222"
			print tok1," is ",tok2 #fixed
			STs.append((str(tok1),"is",str(tok2)))
		if item.keys()[0] in verbRel:
			if values[4]!='O': # ARG
				val1=item.keys()[0]
				#val2=values[4].split("-")[1:]
				val2=values[4]
				damnval2=values[4].split("-")[0]
				val2=val2.replace(damnval2+"-","")
				roleDep.append((val1,val2))
	#print "###########NER#############################"	 #number tags checked		
	#-- 4-4 Translating Args into rolesets, if the Arg is not in allRole list , it's printed itself. 
	#print "\n\nSEnn",Senn,"\n\n"
	for item in roleDep:
		token=item[0]
		role=item[1]
		#number=token.split("-")[-1]
		token=indices[int(token.split("-")[-1])-1] #fixed
		if role in allRoles.keys():
	
			#print "*role_added1*"
			if len(allRoles[role].split(","))>1:	#sometimes we have more than 1 role , I take the first one
				temp=allRoles[role].split(",")[0]
					
				print token," has-role ",temp
				STs.append((str(token),"has-role",temp))

			else:
				print token," has-role ",allRoles[role]
				STs.append((str(token),"has-role",allRoles[role]))
		else:
#
			#print "*role_added2*"
			print token," has-role ",role
			STs.append((str(token),"has-role",role))

 
	#print "###########-ROLE-NAMEs-#############################"

	#-- 5- Stan Translation-----------------------------------
	
	#-- 5-1 Stan list has all dependencies with the single-verb sentence. in this loop I'm finding the root of these depndenies as "verb" for further loops. 
	#print Stan
	for item in Stan:
		#print item
		if item.keys()[0]=='root':
			verb=item.values()[0][1]
			print "verb as root:",verb
			break
	for item in Stan: #removing root dependency
		#print item
		if item.keys()[0]=='root':
			Stan.remove(item)
			break
	#print "000000000000000000000000000000000000000000"
	#print Stan

	#print "**********",targetverb,verb
	#-- 5-2 in some cases there are no verb in sentence , this loop prints statements containing verb and the verb is the root.
	#print "000000000000000000000000000000000000000000"
	stanRoot=verb.split("-")[0]
	sennaPred=targetverb
#	print "verbs: ",targetverb,verb.split("-")[0]
	if (verb !="notfound" and targetverb==verb.split("-")[0]) or (verb !="notfound" and targetverb==verb.split("-")[0]):
		i=0
		for triple in Stan:
			pred=triple.keys()[0]
			tok1=triple.values()[0][0]
			tok1=indices[int(tok1.split("-")[-1])-1] #fixed numbertag
			
			tok2=triple.values()[0][1]
			tok2=indices[int(tok2.split("-")[-1])-1] #fixed numbertag
			#print "\n here*****",tok1,tok2

			#print "verb-tok1-tok2",vlist[0],tok1,tok2
			#print "##\n\n ",tok1,tok2,"\n\n\n"
			#-- 5-2-1 finding the quivalent predicate from dictionary of stanford dependecnies.
			#--       also nsbj,nsujpass are gathered in sbj[] to make verb-dependencies with 
			#	  other tokens directly connected to the verb in obj[]. 
			if pred in dictionary.keys():
				if dictionary[pred]=="subject":	
					sbj[i]=(tok2,tok1)
					i+=1
					#print "subject",sbj
				elif tok1==vlist[0] or tok2==vlist[0]:#collecting objects
					#print "tok1,tok2 : ",tok1,"---",tok2
					if tok1==vlist[0]:
						obj.append([pred,tok2])
					elif tok2==vlist[0]: 
						obj.append([pred,tok1]) 
					#print "object:",obj
				else:	

					#print "**2222"
					print tok1," ",dictionary[pred]," ",tok2
					STs.append((str(tok1),dictionary[pred],str(tok2)))

	
		#-- 5-2-2 printing statments withe predicate --verb-- among subjects and other objects directly connected to verb. 
		#--       the location of each token is mentioned but for the verb it's omitted.  
		print ":::::::::::::::::::::::::::::::::::::::::::::::::;"
		print "subjects All:",sbj # created in previous loop , no need for number fixation
		print "objects", obj
		neg=0
		for ob in obj:
			if 'neg' in ob:
				neg=1
				break

		print "stanford",Stan
		for subject in sbj.values():
			for objects in obj:
				pred=dictionary[objects[0]]
				
				damnVerb=subject[1].split("-")[0]

				if neg==1: damnVerb="not-"+damnVerb
				print "!!!!!!!!!!!!!!!!!damnVerb, neg",damnVerb,neg
				if str(pred)!="is-Arg1" :

					tok1=subject[0]
					tok2=objects[1]

				#	print "**"
					if tok2.split("-")[0]!="not":
						print tok1," ",damnVerb+"-"+str(pred)," ",tok2
						STs.append((tok1,damnVerb+"-"+str(pred),tok2))
				else:
					tok1=subject[0]

					tok2=objects[1]

				#	print "*nbnbn5*"
					if tok2.split("-")[0]!="not":
						print tok1," ",damnVerb," ",tok2
						STs.append((tok1,damnVerb,tok2))

		
		#print STs
	#-- 5-2-3 some sentences in stanford doesn't detect a verb as root. 
	# 	  this is the loop for including relations in sentences without a verb-root
	else:	# tok1 tok2 are coming from stan2nd , so their tag numbers must be fixed
		#print "###########--verb not root" 
		for triple in Stan:
			pred=triple.keys()[0]
			tok1=triple.values()[0][0]
			#print tok1
			tok1=indices[int(tok1.split("-")[-1])-1] #fixed
			#print indices,tok1
			tok2=triple.values()[0][1]
			tok2=indices[int(tok2.split("-")[-1])-1] #fixed
			#print pred,tok1,tok2
			if pred in dictionary.keys():		
				print tok1," ",dictionary[pred]," ",tok2
				STs.append((str(tok1),dictionary[pred],str(tok2)))
	#print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	#print "to numerate: ",result
	sentlist=result.split(" ")
	#print sentlist
	#i=0
	

	newSTs=[]

	#print "888888888888888888888888888888888888888888888888888888"
	#print Poss
	#print sentlist
	#print indices
	if len(Poss)>0:
		for item in STs:
			#print"&*&", item
			sw=0
			i=0
			
			#print len(Poss)
			for poss in Poss: #filling newSTs
				i+=1
				#print "--Pss",poss
				possID=poss[0]
				temp1=poss[1] #john
				temp2=poss[2] #brother
				item0=item[0].replace("-"+item[0].split("-")[-1],"") # item[0] is the token with tagnumber, item0 is the token without tagnumber
				item2=item[2].replace("-"+item[2].split("-")[-1],"") # item[2] is the token with tagnumber, item2 is the token without tagnumber
				#print "--",item0,possID,item2
				if item0==possID and sw==0: # brother -- shopping
					#print "rmoved ",item," appended ",(temp2,item[1],item[2])
					#STs.remove(item)
					#print "if-1"
					num3=sentlist.index(possID)
					#print temp2, indices[num3]
					tup=(temp2+"-"+str(num3+1),"of",temp1+"-"+str(num3))
					#print "tup",tup
					token=item[2] #with n
					
					#print "tupp",(temp2+"-"+str(num3+1),item[1],token)
					newSTs.append((temp2+"-"+str(num3+1),item[1],token))
					sw=1
					if tup not in newSTs:
							newSTs.append(tup)
				elif item2==possID and sw==0:
					#print "removed",item," appended ",(item[0],item[1],temp2)
					#STs.remove(item)
					#print "elif-2"
					token=item[0]
					num3=sentlist.index(possID)
					newSTs.append((token,item[1],temp2+"-"+str(num3+1)))
					
					sw=1	
					tup=(temp2+"-"+str(num3+1),"of",temp1)
					#print "tup**",tup
					if tup not in newSTs:
							newSTs.append(tup)	
				elif item0!=possID and item2!=possID and sw==0 and i==len(Poss):
					#print "elif-3"
					if item not in newSTs: 
						#print "not removed ",item
						t1=item[0] 
						t2=item[2]
						
						#print "tup",(t1,item[1],t2)
						newSTs.append((t1,item[1],t2))
			
				

	if len(newSTs)==0: #newSTs is empty because no Poss has been detected , newSTs was created in the loop above . so if there are no poss-dependencies , newSTs would be the same as STs (tag-numbers are checked)
		newSTs=STs
	



				
	print "all statements", newSTs #!!!!!!!!!!!!!!!!!!!!!!!1checked	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#fixing Dates: dateObjects
	print "------------------------------------------------"
	remlist=[]
	print "dates: ",dateObjects
	if len(dateObjects)>0:
		length=len(newSTs)
		for i in range(0,length): # for not counting newly added tuples
			item=newSTs[i]
			tok1=item[0]
			pred=item[1]
			tok2=item[2]
			#i=newSTs.index(item)
			#print item
			sw=0
			for date,vals in dateObjects.items():
				if (tok1==vals[0] or tok1==vals[1] or tok1==vals[2]) and ( tok2==vals[0] or tok2==vals[1] or tok2==vals[2]): # I don't want to include this tuple
					remlist.append(item)
				else:
					if tok1==vals[0] or tok1==vals[1] or tok1==vals[2] : 
						#print "to remove:",item, " to append: ",(date,pred,tok2)
						if (date,pred,tok2) not in newSTs: newSTs.append((date,pred,tok2))
						remlist.append(item)
					elif tok2==vals[0] or tok2==vals[1] or tok2==vals[2]:
						#print "to remove:",item, " to append: ",(tok1,pred,date)
						if (tok1,pred,date) not in newSTs : newSTs.append((tok1,pred,date))
						remlist.append(item)
		remlist=list(set(remlist))
		#print "remlist: ",remlist
		#print "before: ",newSTs
		for item in remlist:
			#print item
			newSTs.remove(item)
		newSTs=list(set(newSTs))	
		#print "After: ",newSTs
	print newSTs
	print "********///"
	newSTs+=typeOfs(Stan,indices)
	return newSTs,obj,sbj
#------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------------
#Additional statements
def ExtraSTs(newSTs,PrSent,vlist,addArgs,objects,subjects,DCT):
	
	PrSent=PrSent.replace(",","")
	PrList=PrSent.split(" ")
	modSTs=[]
	print "--**--ExtraSTs"
	#print "objects : ",objects
	#print PrList
	#print "Vlist: ",vlist
	print " to add args: ",addArgs
	print DCT
	verb=vlist[0].split("-")[0]
	print verb
	allRoles={}	
	allRoles=roleFinder(verb)
	
	subjects=subjects.values()
	print "all subjects",subjects
	for obj in objects:
		if "not" in obj: verb="not-"+verb
	for item in addArgs:
		tok1=item[0]
		if tok1 not in vlist and tok1.split("-")[0] not in banlist: #not connected to verb-paths
			label=item[1]
			print "label : ",label
			if label=="A0":
				for obj in objects:
					if tok1 in DCT:
						print tok1," ",verb+"-"+dictionary[obj[0]]," ",obj[1]
						newSTs.append((tok1,verb+"-"+dictionary[obj[0]],obj[1]))
			if label=="A1":
				for sbj in subjects:
					if tok1 in DCT:
						print sbj[0]," ",verb," ",tok1
						newSTs.append((sbj[0],verb,tok1))			
			if label in allRoles.keys():
				role=allRoles[label]
				#print "///",label, role
				if tok1 in DCT:
					if role in ["A0","A1","A2","A3","A4","AM"]: tup=(tok1,"is",label)
					else: tup=(tok1,"has-role",role)
					print tup
					newSTs.append(tup)
			else:
				#print "//",label
				if tok1 in DCT:
					print tok1," is ",label
					newSTs.append((tok1,"has-role",label))
	
	#print "--------"
	return newSTs

######################################################################################################################################
######################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------------
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%555%%%%%%%%%%%%%%%%%%%

#----------------------------------------
def verbLinks(vbn,deplist,VBNs):
	vlist=[]
	vlist.append(vbn)
	for item in vlist:
		#print "from vlist : ",item
		for dep in deplist:
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
#recreating the sentence from a list of related words to a verb from the original sentenc.
#
#
def scanVerb(sen,vlist):
	['behind','without','among','is','are','for','by','from','and','in',',','of','with','on','at','under','to','after',"or","beyond","and","for","since","estimated"]
	doublewords=["becasue","instead","such","addition","due","all","rather","well"]
	doublewordlist=[["becasue","of"],["instead","of"], ["such","as"], ["due","to"],["all","but"],["rather","than"]  ]
	triplewords=["addition","well"]
	triplewordslist=[["in","addition","to"],["as","well","as"]]
	sen=sen.replace(","," , ") # should give the same sentence to stanford
	sen=sen.replace(".","")
	sen=sen.replace("  "," ")
	senlist= list(sen.split(" "))
	senlist = [word.strip() for word in senlist] #removing \n from the last toke of the sentence
	#print "senlist : ",senlist
	newsenlist=[]
	newsen=""
	realIndices=[]
	#print vlist

	for i in range(0,len(senlist)):
		#print item,senlist.index(item)+1
		item=senlist[i]
		if item[-2:-1]=="\n": item=item.replace("\n","")
		index=i
		item=item+"-"+str(index+1)
		newsenlist.append(item)
	#print "newsenlist: ",newsenlist
	print "sentence list: ", newsenlist #now i have the whole sentence in form of a list , indexing words
	for item in newsenlist: 
		index=newsenlist.index(item)
		if item in vlist:
			#print item.split("-")[0]
			newsen+=str(item.split("-")[0])+" "
			realIndices.append(item)
		elif item.split("-")[0] in banlist:
			if (index>0 and index<len(newsenlist)): #checking if preposition is between 2 related words
				if( newsenlist[index-1] in vlist and newsenlist[index+1] in vlist): 
					#print "1 ",item.split("-")[0]
					newsen+=str(item.split("-")[0])+" "
					realIndices.append(item)
			if (index==0 or index==len(newsenlist)): #checking if preposition is before related words in the beginning or in the end
				if( newsenlist[index-1] in vlist or newsenlist[index+1] in vlist): 
					#print "2 ",item.split("-")[0]
					newsen+=str(item.split("-")[0])+" "
					realIndices.append(item)
	newsen+=" ."
				
	return realIndices, newsen

#-----------------------------------------

def gephiTranslate(Statements,gephiFile):
	#print Statements
	gephiFile.write("digraph sample {\n")
	#Statements=list(set(Statements))
	print "--gephi",Statements
	for item in Statements:
			node1=item[0]
			edge=item[1]
			node2=item[2]	
	#	print node1,edge,node2
			gephiFile.write("\""+node1+"\""+" -> "+"\""+node2+"\" "+"[ label = \""+str(edge)+"\" ];\n") 
  	gephiFile.write("}\n")


#--------------------------------------------

def nnMerge(toklist): # the list is already sorted
	#fakeIndex=0
	toklist.sort()
	#print toklist	
	length=len(toklist)
	templist=[]
	index1=int(toklist[0][0])
	temp=toklist[0][1] #base
	#print toklist,length,index1
	for i in range(0,length):
		
		#print "round:",i
		#print "index1:",index1
		if i<length-1:
			#print "if: ",i
			index2=int(toklist[i+1][0]) #index of the 2nd token in toklist
			#print "-index2: ",index2
			if index2-index1==1: # to merge
				temp+="-"+toklist[i+1][1]
				index1=index2	
			else:	#not to merge (indices are not continues)
				templist.append(temp)
				#print "added temp:",temp
				temp=toklist[i+1][1] #moving to the 2nd token in list, setting it as base
				index1=index2
		else:
			if temp not in templist:	
				templist.append(temp)
				#print "added temp:",temp
		#print "templist so far:",templist
	return templist

def nnTotypeOf(allSTs):
	#print "---nnTotypeOf--"
	targets={}
	toAdd=[]
	toRem=[]
	for triple in allSTs:
		tok1=triple[0]
		pred=triple[1]
		tok2=triple[2]
		if pred=="--":
			toRem.append(triple)
			#print triple
			index=int(tok2.split("-")[-1])
			tok2=tok2.replace("-"+str(index),"")
			if tok1 in targets.keys():
				targets[tok1].sort()
				targets[tok1].append((index,tok2)) 
			else:
				targets[tok1]=[]
				targets[tok1].append((index,tok2))

	#print targets
	for key,val in targets.items():
		#print"-----"
		#print key
		templist=nnMerge(val)
		for item in templist:
			a=key.split("-")[-1] #removing index of main token
			key1=key.replace("-"+a,"")
			print key," superClassOf ",item+"-"+key1
			toAdd.append((key,"superClassOf",item+"-"+key1))
	#print toAdd	
	return toAdd,toRem


#`````````````````````````````````````````````````````````````````````````
#making serialization formats with fake https

def makeOtherFormats(STs,inputFile):
	f=open(inputFile+'/results.nt',"w")
	for val in STs:
		val0=val[0].replace(" ","_")
		val1=val[1].replace(" ","_")
		val2=val[2].replace(" ","_")
		f.write("<http://"+val0+"> <http://"+val1+"> <http://"+val2+"> .\n")
	f.close() #nt created
	#----------------------------------------------------------------------------------
	#make graph
	graph=Graph()
	graph.parse(inputFile+'/results.nt',format='nt')

	#makin turtle
	f=open(inputFile+'/rdf.ttl','w') 
	s=graph.serialize(format="turtle")
	
	for line in s.split("\n"):
		#line=line.replace("  ","")
		
		line=line.replace(" .","\n")
		line=line.replace(",",";")
		line=line.replace(" "*8,",,")
		line=line.replace(" "*4,",")
		line=line.replace(" ",",")
		print line
		# removing prefixes for making evaluation easier
		pattern1=r"(ns\d*:)" # Captial Names
		match=re.findall(pattern1,line) #symbols
		for item in match:
			toks=item.split(" ")
			newtok=""
			line=line.replace(item,newtok)

		
		line=line.replace(";","")
		line=line.replace("<http://","")
		line=line.replace(">","")
		if "@prefix" not in line and len(line)>1:
			f.write(line+"\n")
	f.close()

	#making rdf/xml
	f=open(inputFile+'/results.rdf',"w")
	s=graph.serialize(format="xml")
	for line in s.split("\n"):
		f.write(line+"\n")
	f.close()


#---------------------------------------------------------
#typeofS
def MyFn(s):
    return s[-1]

def typeOfs(Stan,indices):
	print "''''''''''''''''''''''"
	print indices, Stan
	sts=[]
	typeOfsDic={}
	for item in Stan:
		dep=item.keys()[0]
		if dep=="nn" or dep=="amod":
			head=item.values()[0][0]
			body=item.values()[0][1]
			if head in typeOfsDic.keys():
				typeOfsDic[head].append(body)
			else:
				typeOfsDic[head]=[]
				typeOfsDic[head].append(head)
				typeOfsDic[head].append(body)
	#sorting list items by number tags
	for keys,vals in typeOfsDic.items():
		vals.sort(key=MyFn)
		obj=" ".join(str(x.split("-")[0]) for x in vals)
		gotya=keys.split("-")[-1]
		#print gotya, indices[int(gotya)-1]
		obj=obj.replace(" ","_")
		sts.append((indices[int(gotya)-1],"superClassOf",obj))
	print sts
	return sts

#----------------------------------
#tagNumbers

def tagRem(AllSTs,senNumber):
	ModSTs=[]
	print "OOOOOOOOOOOOOOOOOOOOOOOOOOOO"
	print AllSTs
	tag="Sen"+str(senNumber)+"-"
	checkList=[]
	countList={}
	damnList={}
	item0=""
	item1=""
	item2=""
	number=0
	#damnList contains all terms with their tag numbers
	for item in AllSTs:
		item1=item[0]
		item2=item[2]
		#print item1,item2
		if "-" in item1 :
			print item1
			if item1.split("-")[0] in damnList: 
				damnList[item1.split("-")[0]].append(item1.split("-")[-1])  
			else: 
				damnList[item1.split("-")[0]]=[]
				damnList[item1.split("-")[0]].append(item1.split("-")[-1])
			#print "77777......",damnList
			damnList[item1.split("-")[0]]=list(set(damnList[item1.split("-")[0]]))
			
			

		if "-" in item2 :
			if item2.split("-")[0] in damnList: damnList[item2.split("-")[0]].append(item2.split("-")[-1])  
			else: 
				damnList[item2.split("-")[0]]=[]
				damnList[item2.split("-")[0]].append(item2.split("-")[-1])
			#print "77777......",damnList
			damnList[item2.split("-")[0]]=list(set(damnList[item2.split("-")[0]]))

	
	#print damnList

	for item in AllSTs:
		item1=item[0]
		item2=item[2]
		if "-" in item1:
			term=item1.split("-")[0]
			if len(damnList[term])==1 : item1=tag+str(item1.split("-")[0]) #means the term is not repeated , so tear off the tag number
			else: item1=tag+str(item1) 				       #means the term is reapeated several times, so keep the tag number
		else:
			if item1 not in ["ORG","PER","TMP","MISC","LOC"]: item1=tag+str(item1)  
		#---------------------------	
		if "-" in item2:
			term=item2.split("-")[0]
			if len(damnList[term])==1 : item2=tag+str(item2.split("-")[0])
			else: item2= tag+str(item2)
		else:
			if item2 not in ["ORG","PER","TMP","MISC","LOC"]: item2=tag+str(item2) 
		#---------------------------		
		if ")" not in item2 : ModSTs.append((item1,item[1],item2))
	return ModSTs

#--------------------------------------------------------
def abbreviations(sent,abbFile,indices):
	addedSTs=[]
	print sent
	sent=sent.replace(","," ")
	sent=sent.replace("."," .")

	sentList=sent.split(" ")
	sentList
	print indices
	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%SentList",sentList
	abbfile=open(abbFile,"r")
	getAbb=abbfile.read()
	for line in getAbb.split("\n"):
		if len(line)>0:		
			print line
			items=line.split(" - ")
			item1=items[-1]
			print item1
			if item1 in sentList:
				item2=items[0]
				print item1 , "-" , item2
				for token in indices:
					term=token.split("-")[0]
					if term==item1: item1=token	
				addedSTs.append((item1,"acronym-for",item2))

	return addedSTs

#-----------------------------------------------------------
#Fixing capital name units into space form

def fixCaps(AllSTs,remakeCaps):
	STs=[]
	keys=remakeCaps.keys()
	for item in AllSTs:
		tag=item[0].split("-")[0]
		item1=item[0].split("-")[-1]
		#print "---item1",item1
		dep=item[1]
		item2=item[2].split("-")[-1]
		if item1 in keys: 
			#print "0000itm1",item1,remakeCaps[item1]
			STs.append((tag+"-"+remakeCaps[item1],dep,item[2]))
		if item2 in keys:
			#print "0000itm2",item2 
			STs.append((item[0],dep, tag+"-"+remakeCaps[item2]))
		if item1 not in keys and item2 not in keys:
			STs.append(item)


	return STs


#------------------------------------------------------------
# a specific type of translation for evaluating the reuslts
def evalTrans(STs):
	print ST

#removing tag numbers AGAIN and eliminating AM-s 
def refineSts(STs):
	newSTs=[]
	for item in STs:
		val0=item[0]
		val1=item[1]
		val2=item[2]
		if "Sen" in val0:
			rem=val0.split("-")[0]
			val0=val0.replace(rem+"-","")
		if "Sen" in val2:
			rem=val2.split("-")[0]
			val2=val2.replace(rem+"-","")
		if "AM-" in val2 :
			if val2 in ["AM-LOC", "AM-DIR","AM-TMP","AM-PNC","AM-CAU"]:
				newSTs.append((val0,val1,val2))
		else:
			newSTs.append((val0,val1,val2))
	return newSTs



