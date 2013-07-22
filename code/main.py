import sys
import os
from StanSennaClass import SenSta
from sennaProcessed import modifySenna
from stanfProcessed import modifyStanf
from code import verbRelatives,roleFinder,translateSent,verbLinks,scanVerb,gephiTranslate,ExtraSTs, nnTotypeOf, makeOtherFormats, tagRem ,abbreviations, fixCaps ,evalTrans, refineSts
import re
from FindPropArg import Find_Pred_Arg_Root,Find_ArgDom_MixArgDep
#------------------------------------------------------------------------------------------------------------------------------------
######################################################################################################################################
######################################################################################################################################
######################################################################################################################################
#------------------------------------------------------------------------------------------------------------------------------------
#-- 1- starting point: a processed sentence is taken from stanford parser, this sentence is in natural form. the same happens for senna.
#-- 2- by using senna file I collect all tokens marked as VB in one list "VBNS"
#-- 3- all dependencies along with the name-of-relation , token1 and token2 are then collected from stanford file in "Preps".
#-- 4-  
#-- 5- for each verb in VBNs all tokens are collected in a vlist, the sentence is then recreated from the original sentence by scanVerb function, and is sent #      to translateSent to build statements. 

path="/home/kimia/srl/"

if __name__=="__main__":
	
	

	#removing comma between digits
	sentence=open(path+"SemanticRoleMiner/code/input/test_input.txt","r")	
	text=sentence.readline()
	keepOrgSent=text
	sentence.close()
	patternComma=r'\d+[,]'
	match=re.findall(patternComma,text) #removing comma in betweeb digits
	for item in match:
		digits=item.replace(",","")
		text=text.replace(item,digits)	
	sentence=open(path+"SemanticRoleMiner/code/input/test_input.txt","w")

	#make all the space-separated capital names 1 unit-name
	remakeCaps={}
	patternCaps=r'(([A-Z][a-z]+\s((of|and|for)\s)*)*[A-Z][a-z]+)'
	match=re.findall(patternCaps,text)
	for item in match:
		temp=item[0]
		temp=temp.replace(" ","")
		temp2=item[0].replace(" ","_")
		remakeCaps[temp]=temp2
		print remakeCaps
		text=text.replace(item[0],temp)
	#print text successfully done

	#removing ,and or , and
	patternAnd=r'([,]\s*(and))'
	match=re.findall(patternAnd,text) #symbols
	for item in match:
		text=text.replace(item[0],"and")
	

	#lowercase beginning for this set
	patternCaptialNoises=r'^(They\s|The\s|A\s|There\s|For\s|From\s|So\s|Then\|She\s|He\s|I\s|That\s|Is\s|Are\s|An\s|This\s|It\s|Am\s)'
	match=re.findall(patternCaptialNoises,text) #symbols
	for item in match:
		text=text.replace(item,item.lower())



	
	
	sentence.write(text)
	sentence.close()
	#------------------------------------------------------------------------------------

	sentence=open(path+"SemanticRoleMiner/code/input/test_input.txt","r")	
	sent=sentence.readline()
	sentence.close()
	OrgSent=sent




	#handling 's
	inputFile="srl/SemanticRoleMiner/code/input"
	myTestFile=SenSta(inputFile)
	myTestFile.makeStanf()	
	stanfile=path+"SemanticRoleMiner/code/input"+"/stanoutput.txt"
	Stan=modifyStanf(stanfile)
	
	# Fixing 's, using poss dependecy , it Only works if stanford recognizes poss dependecy
	Poss=[]
	for key,val in Stan.items():
	    for i, prep in val.items():
		pred=prep.keys()[0]
		rel=prep.values()[0]
		token1=rel[0]
		token2=rel[1]
		if pred=="poss":
			Poss.append((str(token2.split("-")[0])+str(token1.split("-")[0]),str(token2.split("-")[0]),str(token1.split("-")[0])))
			#print "***********Posessins: ",Poss
			sent=sent.replace(str(token2.split("-")[0])+"'s "+str(token1.split("-")[0]),str(token2.split("-")[0])+str(token1.split("-")[0]))
	#print sent



	#find and replace Captial Names attached
	pattern1=r"\s\s" # removing extra spaces
	pattern2=r"(\"|\'|\s\s|\_)"
	pattern3=r"([A-Z]\w+\s)" # Captial Names
	
	match=re.findall(pattern2,sent) #symbols
	for item in match:
		toks=item.split(" ")
		newtok=" "
		sent=sent.replace(item,newtok)
		
	#print "symbls removed : ",sent
	

	ofpattern=r'[A-Z][a-z]+\sof\s[A-Z][a-z]+'
	match=re.findall(ofpattern,sent)
	for item in match: 
#		print item
		item2=item.split(" of ")
#		print item2
		sent=sent.replace(" of "+item2[1],"")
		sent=sent.replace(item2[0],item2[0]+"of"+item2[1])
	match=re.findall(pattern3,sent) #capitals
	match=match[0:-1]   # the last token in pattern usually captures a low letter name 
	templist=sent.split(" ")
	#print templist
	if len(match)>1:
		for item in match:
			toks=item.split(" ")
			check=templist.index(toks[0])+1
			#print templist[check], templist[check][0].isupper()
			if templist[check][0].isupper(): 
				#print "()()()()",toks
				newtok=''.join(toks)
				sent=sent.replace(item,newtok)
				
			
	#replacing whats and what is with the reason
	whatpattern=r"\s(what's|what is)\s"
	match=re.findall(whatpattern,sent)
	for item in match:
		sent=sent.replace(item," the reason ")	
	
	PrSent=sent #processed sentence
	sent=sent.replace(" s "," ") # when poss-dependency is not available  the 's is leaving a "s" alone , so I treat it as nn dependency and remove s 
	print "###---processed sent:",PrSent

	#print sent to process original sentence pre-processed
	sentence=open(path+"SemanticRoleMiner/code/input/test_input.txt","w")	
	sentence.write(sent)
	sentence.close()

	inputFile="srl/SemanticRoleMiner/code/input"
	myTestFile=SenSta(inputFile)
	myTestFile.makeSenna()
	myTestFile.makeStanf()
	sennafile=path+"SemanticRoleMiner/code/input"+"/sennaoutput.txt"
	
	stanfile=path+"SemanticRoleMiner/code/input"+"/stanoutput.txt"


#*************************************************************
	# testing Feb 19th , additional statements
	SEN0_SE=myTestFile.sennaDict['sen0']
	SEN0_ST=myTestFile.stanfDict['sen0']
	PAR=Find_Pred_Arg_Root(myTestFile,SEN0_SE,SEN0_ST)
	PRED=PAR[0]
	ARGS=PAR[1]
	#print "^^^^^^^^^^^^^^^^^^^^^^pred",PRED
	#print ARGS.values()
	ARGs=ARGS.values()
	#print "****--***",PRED
	addArgs={}
	for vals in PRED.values():
	#	print vals,vals.split("-")[0]
		addArgs[vals]=[]
	#print addArgs #{'amending-32': [], 'called-19': []}
	#print "&&--alARGS",ARGs
	for item in ARGs:
		lb="not-found" #finding each list verb along number-tag 
		for key,val in item.items():
	#		print key,",",val
			label=key.split("-")[0]
			if label=="V":
				lb=val[0][0]
				break
		if lb !="not-found":
			#print"&&--", item
			for key,val in item.items():
				#print key,"--",val
				key2=key.replace("-"+key.split("-")[-1],"")
				if key.split("-")[0]!="V":
					for v in val:
						if v[0].split("-")[0]!=",":
	#						print key,v[0]
							temp=key.split("-")[-1]
							#print "--",key
							key=key.replace("-"+temp,"")
							#print"-", v[0],temp,key2
							addArgs[lb].append((v[0],key2))		
	#print addArgs
	print "##################################################"
#*************************************************************
#*************************************************************
	
	quote=r"(.,\s(\w+)\ssaid\s*)."
	addLast=[]
	match=re.findall(quote,sent)
	#print match[0][0]
	if len(match)>0:
		sayer=match[0][-1]
		#I should add the arguments related to said in here
		#I'm gonna translate this as he-is-sayer , he-said-statement , statement-begins_with-We , we is the beginning of statement
		sent=sent.replace(match[0][0]," ")
		beginStatement=sent.split(" ")[0]
	
		addLast.append((sayer,"is","Sayer"))
		addLast.append((sayer,"said","Statement"))
		addLast.append(("Statement","begins_with",beginStatement))
	
		sentence=open(path+"SemanticRoleMiner/code/input/test_input.txt","w")	
		sentence.write(sent)
		sentence.close()

		inputFile="SemanticRoleMiner/code/input"
		myTestFile=SenSta(inputFile)
		myTestFile.makeSenna()
		myTestFile.makeStanf()
		sennafile=path+"SemanticRoleMiner/code/input"+"/sennaoutput.txt"
		stanfile=path+"SemanticRoleMiner/code/input"+"/stanoutput.txt"	
#*************************************************************
	#2
	Senna=modifySenna(sennafile)
	#print Senna['sen0']
	
	VBNs=[]
	for sen,val in Senna.items():
		for num,token in val.items():
			for a,b in token.items():
				if b[1][0:2]=="VB":
					VBNs.append(a)

	#print VBNs
	#3
	Stan=modifyStanf(stanfile)
	Preps={}
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
	
	#4
	vals=Stan.values()[0]
	temp=vals.values() 
	#print temp
	#print VBNs 
	#DCT={} #directly connected tokens
	#VBs=list(set(VBNs+PRED.values()))
	DCT=[]
	#for v in VBNs:
	#	DCT[v]=[]
	print "888888888"
	for v in vals.values():
		prep=v.keys()[0]
		toks= v.values()[0]
		tok1=toks[0]
		tok2=toks[1]
		if prep.split("_")[0]!="prep" and tok1 in VBNs and tok2 !="ROOT-0" and tok2 not in VBNs:
			DCT.append(tok2)
		elif prep.split("_")[0]!="prep" and tok2 in VBNs and tok1 !="ROOT-0" and tok1 not in VBNs:
			DCT.append(tok1)
		
	allDeps=[] 
	for v in temp:
		a=(v.values()[0][0],v.values()[0][1])
		if a not in allDeps:
			#print a
			allDeps.append(a)

	#print "allDeps ", allDeps

	#5
	sen=[]
	#print VBNs
	output=open(path+"SemanticRoleMiner/code/input/results.txt",'w')
	output.write("-Complete Sentence is: \n"+OrgSent+"\n")
	output.write("----------------------------------------------------------------------\n")
	output.write("----------------------------------------------------------------------\n")
	
	evaloutput=open(path+"SemanticRoleMiner/code/input/eval_result.txt","w")	
	evaloutput.write(keepOrgSent+"\n")

	SennaStan=open(path+"SemanticRoleMiner/code/input/Stan_Senna_results.txt",'w')





	sentNumber=1
	AllSTs=[]
	gephiFile=open(path+"SemanticRoleMiner/code/input/gephi.dot","w")
	for vbn in VBNs:
		#vbn="isolated-18"
		#print"to be :  "
		print "((((here is the VBN:))))",vbn
		vlist=verbLinks(vbn,allDeps,VBNs)
		#print "to be vlist:",vlist
		#print "vlist: ",vlist

		if len(vlist)>1:
		#	print vlist
			STs=[]
			
			(indices,result)=scanVerb(sent,vlist)
			#print "result: ",result # here is the new sentece, segmented from the original one.
			#print "indices:", indices
			#-- writing each sentence along with their triples in results.txt
			output.write(str(sentNumber)+"-"+result+"\n\n")
			SennaStan.write(str(sentNumber)+"-"+result+"\n\n")
			sen.append(result)
			#print indices
			(STs,objs,sbjs)=translateSent(vlist,result,Poss,indices,PrSent)
			print "\n\n************************\n",STs,"\n****************\n"
				#print "before LOOOP",vbn, PRED.values()
			if vbn in PRED.values(): #some of the VBNs are not recognised as verb in the 1st senna output #testcase4 (prepared)
			#	print "######",addArgs[vbn]
				moreSTs=ExtraSTs(STs,PrSent,vlist,addArgs[vbn],objs,sbjs,DCT)
				STs=list(set(STs+moreSTs)) # added roles from missing part of sentence (cause:verbToverb connection)
			#----------------------- adding abbreviation
			abbFile=path+"SemanticRoleMiner/code/input/abbreviation.txt"
			abbr=abbreviations(sent,abbFile,indices)
			STs+=abbr
			(toAdd,toRem)=nnTotypeOf(STs)
			STs=list(set(STs)-set(toRem))
			
			STs=list(set(STs+toAdd))
			for st in STs: 
				if "(" not in st[2] and "*" not in st[2] and ")" not in st[2]:
					output.write("      "+str(st[0])+"  "+str(st[1])+"  "+str(st[2])+"\n")
					#evaloutput.write("      "+str(st[0])+"  "+str(st[1])+"  "+str(st[2])+"\n")
			#-----------------------
			
			output.write("          --------------------------------------------------          \n")

			#-- writing each sentence stanford output in Stan_Senna_results.txt
			stanfile=open(path+"SemanticRoleMiner/code/stanoutput.txt","r")
			text=stanfile.read()
			stanfile.close()
			SennaStan.write("-Stanford Output: ----------------------------------------------------\n")
			SennaStan.write(text)
			#-- writing each sentence ssenna output in Stan_Senna_results.txt
			sennafile=open(path+"SemanticRoleMiner/code/sennaoutput.txt","r")
			text=sennafile.read()
			sennafile.close()
			SennaStan.write("--Senna Output:------------------------------------------------------ \n")
			SennaStan.write(text)
			SennaStan.write("----------------------------------------------------------------------\n")
			AllSTs=list(set(AllSTs+STs))
			sentNumber+=1
			#typeOfs(Stan)
	AllSts+=addLast
	Results=open(path+"SemanticRoleMiner/code/input/RESULTS.txt","w")
	for item in AllSTs:
		Results.write(item[0]+"  -"+item[1]+"-  "+item[2]+"\n")
	Results.close()
	initfile=open(path+"SemanticRoleMiner/code/input/init.txt","r")
	#print "initiiiiiii"
	senNumber= int(initfile.readline().split("\n")[0])
	#print "\n\n",AllSTs,"\n\n"
	initfile.close()
	AllSTs=tagRem(AllSTs,senNumber)
	#print "---LAST MODIFICATION"
	AllSTs=fixCaps(AllSTs,remakeCaps)
	#print AllSTs
	gephiTranslate(AllSTs,gephiFile)
	#print "Statements:",STs
	
	SennaStan.close()
	output.close()
	gephiFile.close()
	
	#---fixing input file for this process has modified it
	sentence=open(path+"SemanticRoleMiner/code/input/test_input.txt","w")	
	sentence.write(keepOrgSent)
	sentence.close()
	inputFile=path+"SemanticRoleMiner/code/input"
	
	#print DCT, PRED.values()
	#print DCT, PRED.values()
	print "\n\n"
	print "raw:\n",AllSTs
	refinedSTs=refineSts(AllSTs)
	print "refined:\n",refinedSTs
	AllSTs=[]
	AllSTs=refinedSTs
	makeOtherFormats(AllSTs,inputFile)

	
	#translating for evalutation, checking if they have tag numbers
	print "-----------------ALL ATS-----------------"
	for st in AllSTs:
		evaloutput.write("<"+str(st[0])+" ; "+str(st[1])+" ; "+str(st[2])+">\n")
	evaloutput.write("---------\n")
	evaloutput.close()
