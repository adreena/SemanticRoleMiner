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
i=0
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
#print sentences_Senna["sen1"]





