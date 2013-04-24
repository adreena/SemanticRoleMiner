import os

#initialization
outputFile=open("/home/mgr/SemanticRoleMiner/code/input/tokyo/Allresult.txt","w")
outputFile.close()
SennaStan=open("/home/mgr/SemanticRoleMiner/code/input/tokyo/Stan_Senna_results.txt",'w')
SennaStan.close()
count=1
tokyo=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/tokyo/tokyo.txt","r")
txt=tokyo.read()
txt=txt.replace(";"," .\n")
counter=-1
for line in txt.split("\n"):
  #print count	
	counter+=1
	if len(line)>1:
		inputFile=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/test_input.txt","w")
		inputFile.write(line)
		inputFile.close()
		initfile=open("/home/kimia/srl/SemanticRoleMiner/code/input/init.txt","w")
		initfile.write(str(counter))
		initfile.close()
		print line
		cmd=os.system('python main.py')
		result=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/results.txt","r")
		getall=result.read()
		#print getall
		outputFile=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/tokyo/Allresult.txt","a")
		outputFile.write("Sentence: "+str(count)+"\n"+"*********************************************\n")
		#outputFile.write(line)
		outputFile.write(getall+"\n")
		outputFile.close()
		
		ss=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/Stan_Senna_results.txt",'r')
		getall=ss.read()
		SennaStan=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/tokyo/Stan_Senna_results.txt",'a')
		SennaStan.write("Sentence: "+str(count)+"\n"+"*********************************************\n")
		SennaStan.write(getall+"\n")
		SennaStan.close()

		gg=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/gephi.dot","r")
		getall=gg.read()
		gephi=open("/home/kimia/srl/python/SemanticRoleMiner/code/input/tokyo/gephi"+str(count)+".dot","w")
		gephi.write(getall)
		gephi.close()

		count+=1
