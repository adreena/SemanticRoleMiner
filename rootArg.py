import linecache


#required files as 2 main input to this program

file_stanford_input = open('/home/kimia/srl/stanford-parser/tests/output1.txt','r')
file_senna_input    = open('/home/kimia/srl/senna/tests/output1.txt','r')
stanIterator    =file_stanford_input.read()
sennaIterator   =file_senna_input.read()

sennalines=open('/home/kimia/srl/senna/tests/output1.txt').readlines()
file_stanford_input.close()
file_senna_input.close()

sentences_Stan={}
i=-1
#separating sentences by iterator
for line in stanIterator.split("\n"):
    
   #First
   #sentence detected , create a key in sentences dictionary
    if line=="(ROOT":	 
	i+=1        
	sentences_Stan['sen'+str(i)]={}
   #Second 
   #finding root and its index of each sentences detected    
    if line[0:4]=="root":
       root=line.replace(",","")
       root=root.replace("("," ")
       root=root.replace("-"," ") 
       root=root.replace(")","")
       root=root.split(" ")
       index=root[-1]
       root=root[-2]
       sentences_Stan["sen"+str(i)]["root"]=root
   #Third , now root detected 
   #going to sennaIterator to find target column
#output of stanford 
#2 sentences are identified sentences_Stan={'sen2': {'root': 'sanitized'}, 'sen1': {'root': 'have'}}
#for each a root is found       

#------------------------------------------------------------------------------------------------------------------
#preprocessing senna file
j=0
sentences_Senna={}
sentences_Senna["sen0"]={}
for line in sennaIterator.split("\n"):
   tokens=line.replace(" ","")
   tokens=tokens.replace("\t","|")
   tokens=tokens.split("|")
   #print tokens
   if tokens[0]!=".": 
        counter=0
        sentences_Senna["sen"+str(j)][tokens[0]]={}
	for element in tokens[1:]:
	    print element
	    sentences_Senna["sen"+str(j)][tokens[0]][counter]=element

	    counter+=1
   else: 
     j+=1 
     print "end"
     sentences_Senna["sen"+str(j)]={}
      

print sentences_Stan
print sentences_Senna["sen0"]["Tanks"]
print sentences_Senna["sen0"]["used"]
print sentences_Senna["sen1"]["Sand"]
# outputs of senna proccess
# 2 sentences are identified sentences_senna{"sen0"={"Tanks"={"0"=NNS,...},"used"={"0"=VBN,...}}, "sen1"={"Sand"={...},"and"={}, "activated={}"}}
#sentences_Senna["sen0"]["Tanks"] => {0: 'NNS', 1: 'S-NP', 2: 'O', 3: '-', 4: 'S-A0', 5: 'B-A0', 6: '(S1(S(NP(NP*)'}
#sentences_Senna["sen0"]["used"]  => {0: 'VBN', 1: 'S-VP', 2: 'O', 3: 'used', 4: 'S-V', 5: 'I-A0', 6: '(VP*'}
#sentences_Senna["sen1"]["Sand"]  => {0: 'NN', 1: 'S-NP', 2: 'S-PER', 3: '-', 4: 'O', 5: 'O', 6: 'B-A1', 7: 'O', 8: 'O', 9: '(S1(S(NP*)'}






