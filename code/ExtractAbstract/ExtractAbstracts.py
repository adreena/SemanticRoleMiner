import sys
import os
import re

abstractFile=open("/home/kimia/srl/SemanticRoleMiner/code/Allabs/49abstracts.txt","r")
abstractOutput=open("/home/kimia/srl/SemanticRoleMiner/code/Allabs/ExAbOutput.txt","w")
counter=1
stop=counter+3
abstractFileRead=abstractFile.read()

for line in abstractFileRead.split("\n"):
	if line[0:3]=="Abs":
		abstractOutput.write(line+"\n****\n")
		#if [! -d ""]; then 
		cmd=os.system('if [ ! -d abstract'+str(counter)+' ]; then mkdir abstract'+str(counter)+'; fi')
		abbreviationFile=open("/home/kimia/srl/SemanticRoleMiner/code/Allabs/abstract"+str(counter)+"/abbreviation.txt","a")
		abbreviationFile.close()
		#cmd=os.system('mkdir '+"abstract"+str(counter)) #create a folder for every abstract 
		ExtractedAbsFile=open("/home/kimia/srl/SemanticRoleMiner/code/Allabs/abstract"+str(counter)+"/test_input.txt","w")
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
		AbrPattern=r'((((([A-Z][a-z]+\s((in|for|of|and)\s)*)*[A-Z][a-z]+)(\Ss)*\s))(\([A-z]+\)))' #item[0] must be removed, item[-1] instead is kep as the short form
		match=re.findall(AbrPattern,line)
		abbreviationFile=open("/home/kimia/srl/SemanticRoleMiner/code/Allabs/abstract"+str(counter)+"/abbreviation.txt","w")
		for item in match:
			ab=item[-1]
			ab=item[-1].replace("(","")
			ab=ab.replace(")","") 
			print item
			abbreviationFile.write(item[1]+"- "+item[-1][1:-1]+"\n" )
			line=line.replace(item[0],ab)
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
		ExtractedAbsFile.close()
		#NOW running translateParagraph.py for parsing the whole paragraph
		paragraphNumber=open("/home/kimia/srl/SemanticRoleMiner/code/input/paragNumber.txt","w")
		paragraphNumber.write(str(counter))
		paragraphNumber.close()
		print line
		cmd=os.system('python /home/kimia/srl/SemanticRoleMiner/code/translateParagraph.py')
		
		
		counter+=1
	if counter==stop: break

abstractFile.close()
abstractOutput.close()
print counter		
		
		
