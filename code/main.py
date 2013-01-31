import sys
import os
from StanSennaClass import SenSta
from sennaProcessed import modifySenna
from stanfProcessed import modifyStanf
from code import verbRelatives,roleFinder,translateSent,verbLinks,scanVerb

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

	
	print sent
	inputFile="srl/python/SemanticRoleMiner/code/input"
	myTestFile=SenSta(inputFile)
	myTestFile.makeSenna()
	myTestFile.makeStanf()
	sennafile="/home/kimia/srl/python/SemanticRoleMiner/code/input"+"/sennaoutput.txt"
	
	stanfile="/home/kimia/srl/python/SemanticRoleMiner/code/input"+"/stanoutput.txt"
	
	

	#2
	Senna=modifySenna(sennafile)
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
	
	#print Preps


	#4
	vals=Stan.values()[0]
	temp=vals.values() 
	#print "*" 
	allDeps=[] 
	for v in temp:
		a=(v.values()[0][0],v.values()[0][1])
		if a not in allDeps:
			#print a
			allDeps.append(a)

	#print allDeps

	#5
	sen=[]
	#print VBNs
	for vbn in VBNs:
		#vbn="isolated-18"
		vlist=verbLinks(vbn,allDeps,VBNs)
		
		print vlist
		if len(vlist)>1:
			result=scanVerb(sent,vlist)
			print result
			sen.append(result)
			translateSent(vlist,result)
		
	 	#break
	 
	



