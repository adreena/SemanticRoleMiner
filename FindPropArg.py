#Goal : For each sentence args for a root are investigated

def findArg((index,root),targetDict):
    
     tokenLabels={}
     Labels={}
    #--Testing function arguments Perfect working
     #print index
     #print root
     #print targetDict

     #--Finding the target column for retreiving correct args
     #--going through root element to find where predicate has happened its column is marked as 'V'
     #--I take all elements of root row and check for detection of V 
     #--to mark its id as target column

     targetColumn='Null'
     for element_id in targetDict[int(index)][root]:
         #print element_id
         #print targetDict[int(index)][root][element_id]
         take=targetDict[int(index)][root][element_id]
         #print take
         #print take[-1] trying to find V in S-V as verb
         if take[-1]=="V":
            #print element_id
            targetColumn=element_id

     #sanityCheck of right column Id 
     #print targetDict[int(index)][root]
     #tok=targetDict[1]
     #print tok
     #for key in tok:
         #print tok[key][targetColumn]
     

     # having all args for all tokens  
     for key in targetDict:
         token=targetDict[key]
         #--token is now a dictionary 
         #print token
         for word in token:
            #print targetDict[key][word][targetColumn]
            modify=targetDict[key][word][targetColumn]
            temp=modify.split('-')
            #print temp
            #print temp[1]
            #print word 
            #tokenLabels[word]=temp[1]
            if temp[1] in tokenLabels:
               tokenLabels[temp[1]].append(word)
            else:
               tokenLabels[temp[1]]=[]
               tokenLabels[temp[1]].append(word) 
          
     #tokenLabels['Tanks']='A0'
     print tokenLabels





