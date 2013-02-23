import sys
import os
from StanSennaClass import SenSta
from sennaProcessed import modifySenna
from stanfProcessed import modifyStanf
from code import verbRelatives,roleFinder,translateSent,verbLinks,scanVerb,gephiTranslate,ExtraSTs, nnTotypeOf
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



if __name__=="__main__":

	#1
	sentence=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/test_input.txt","r")	

	sent=sentence.readline()
	sentence.close()

	OrgSent=sent
	#handling 's

	inputFile="srl/python/SemanticRoleMiner/code/input"
	myTestFile=SenSta(inputFile)
	myTestFile.makeStanf()	
	stanfile="/home/kimia/srl/python/SemanticRoleMiner/code/input"+"/stanoutput.txt"
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
				
			
	
	PrSent=sent #processed sentence
	sent=sent.replace(" s "," ") # when poss-dependency is not available  the 's is leaving a "s" alone , so I treat it as nn dependency and remove s 
	print "###---processed sent:",PrSent

	#print sent to process original sentence pre-processed
	sentence=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/test_input.txt","w")	
	sentence.write(sent)
	sentence.close()

	inputFile="srl/python/SemanticRoleMiner/code/input"
	myTestFile=SenSta(inputFile)
	myTestFile.makeSenna()
	myTestFile.makeStanf()
	sennafile="/home/kimia/srl/python/SemanticRoleMiner/code/input"+"/sennaoutput.txt"
	
	stanfile="/home/kimia/srl/python/SemanticRoleMiner/code/input"+"/stanoutput.txt"


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
	DCT={} #directly connected tokens
	for v in VBNs:
		DCT[v]=[]
	for v in vals.values():
		toks= v.values()[0]
		tok1=toks[0]
		tok2=toks[1]
		if tok1 in VBNs and tok2 !="ROOT-0" and tok2 not in VBNs:
			DCT[tok1].append(tok2)
		elif tok2 in VBNs and tok1 !="ROOT-0" and tok1 not in VBNs:
			DCT[tok2].append(tok1)
	#print DCT	
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
	output=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/results.txt",'w')
	output.write("-Complete Sentence is: \n"+OrgSent+"\n")
	output.write("----------------------------------------------------------------------\n")
	output.write("----------------------------------------------------------------------\n")
	
	SennaStan=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/Stan_Senna_results.txt",'w')





	sentNumber=0
	AllSTs=[]
	gephiFile=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/gephi.dot","w")
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
			print "result: ",result # here is the new sentece, segmented from the original one.
			print "indices:", indices
			#-- writing each sentence along with their triples in results.txt
			output.write(str(sentNumber)+"-"+result+"\n\n")
			SennaStan.write(str(sentNumber)+"-"+result+"\n\n")
			sen.append(result)
			#print indices
			(STs,objs,sbjs)=translateSent(vlist,result,Poss,indices,PrSent)
			#print STs
			print "before LOOOP",vbn, PRED.values()
			if vbn in PRED.values(): #some of the VBNs are not recognised as verb in the 1st senna output #testcase4 (prepared)
				print "######",addArgs[vbn]
				moreSTs=ExtraSTs(STs,PrSent,vlist,addArgs[vbn],objs,sbjs,DCT)
				STs=list(set(STs+moreSTs)) # added roles from missing part of sentence (cause:verbToverb connection)
			(toAdd,toRem)=nnTotypeOf(STs)
			STs=list(set(STs)-set(toRem))
			STs=list(set(STs+toAdd))
			for st in STs: output.write("      "+str(st[0])+"  "+str(st[1])+"  "+str(st[2])+"\n")
			
			output.write("          --------------------------------------------------          \n")

			#-- writing each sentence stanford output in Stan_Senna_results.txt
			stanfile=open("/home/kimia/srl/python/SemanticRoleMiner/code/stanoutput.txt","r")
			text=stanfile.read()
			stanfile.close()
			SennaStan.write("-Stanford Output: ----------------------------------------------------\n")
			SennaStan.write(text)
			#-- writing each sentence ssenna output in Stan_Senna_results.txt
			sennafile=open("/home/kimia/srl/python/SemanticRoleMiner/code/sennaoutput.txt","r")
			text=sennafile.read()
			sennafile.close()
			SennaStan.write("--Senna Output:------------------------------------------------------ \n")
			SennaStan.write(text)
			SennaStan.write("----------------------------------------------------------------------\n")
			AllSTs=list(set(AllSTs+STs))
			sentNumber+=1
	gephiTranslate(AllSTs,gephiFile)
	#print "Statements:",STs
	
	SennaStan.close()
	output.close()
	gephiFile.close()
	
	#---fixing input file for this process has modified it
	sentence=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/test_input.txt","w")	
	sentence.write(OrgSent)
	sentence.close()
