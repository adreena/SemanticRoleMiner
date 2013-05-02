import sys
import os
import re

abstractFile=open("/home/kimia/srl/SemanticRoleMiner/code/abstracts/49abstracts.txt","r")
abstractOutput=open("/home/kimia/srl/SemanticRoleMiner/code/abstracts/ExAbOutput.txt","w")
counter=1
abbreviationFile=open("/home/kimia/srl/SemanticRoleMiner/code/abstracts/abstract_"+str(counter)+"/abbreviation.txt","w")
abbreviationFile.close()

abstractFileRead=abstractFile.read()

for line in abstractFileRead.split("\n"):
  if line[0:3]=="Abs":
		abstractOutput.write(line+"\n****\n")
		#if [! -d ""]; then 
		cmd=os.system('if [ ! -d abstract_'+str(counter)+' ]; then mkdir abstract_'+str(counter)+'; fi')
		#cmd=os.system('mkdir '+"abstract_"+str(counter)) #create a folder for every abstract 
		ExtractedAbsFile=open("/home/kimia/srl/SemanticRoleMiner/code/abstracts/abstract_"+str(counter)+"/test_input.txt","w")
		line=line.replace("[","")
		line=line.replace("]","")
		#pattern for noise capital letters
		patternCaptialNoises=r'(\.\s)*(The\s|A\s|There\s|She\s|He\s|I\s|That\s|Is\s|Are\s|An\s|This\s|It\s|Am\s)'
		match=re.findall(patternCaptialNoises,line) #symbols
		#print line+"\n"
		for item in match:
			line=line.replace(item[-1],item[-1].lower())
		#print line
		#pattern 3
		AbrPattern=r'((((([A-Z][a-z]+\s(of\s)*)*[A-Z][a-z]+)\s))(\([A-z]+\)))' #item[-1] must be removed, item[1] is the compelte name
		match=re.findall(AbrPattern,line)
		abbreviationFile=open("/home/kimia/srl/SemanticRoleMiner/code/abstracts/abstract_"+str(counter)+"/abbreviation.txt","a")
		for item in match: 
			abbreviationFile.write(item[1]+"- "+item[-1][1:-1]+"\n" )
			line=line.replace(item[-1],"")
		abbreviationFile.close()
		# pattern 1
		RefPattern=r'(References: \d+)' #removing [References: dd] from text
		match=re.findall(RefPattern,line)
		for item in match: line=line.replace(item,"")
		


# pattern 2
		ListPattern=r'\w+\:\s' #removing : , example : covers 11 zoonotic agents :  Salmonella --> covers 11 zoonotic agents are  Salmonella, 
		match=re.findall(ListPattern,line)
		for item in match: line= line.replace(item[-2:-1]," are ")


		
		
		ExtractedAbsFile.write(line[14:]) # removing "Abstract: "
		#NOW running translateParagraph.py for parsing the whole paragraph
		paragraphNumber=open("/home/kimia/srl/SemanticRoleMiner/code/input/paragNumber.txt","w")
		paragraphNumber.write(str(counter))
		paragraphNumber.close()
		cmd=os.system('python /home/kimia/srl/SemanticRoleMiner/code/translateParagraph.py')
		
		
		counter+=1
		

abstractFile.close()
abstractOutput.close()
print counter		
		
		
