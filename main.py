#importing SenSta class for creating 
from StanSennaClass import SenSta
from FindPropArg import findArg
from FindPropArg import findPreds
from FindPropArg import mixDepArg
from FindPropArg import findDomain
from CreateRelations import makeRel
from CreateRelations import makeSt0
from CreateRelations import makeSt
from CreateRelations import makeSubSt
from CreateRelations import verbDepArg
from Visualizer import makeGephi


#working with class object myTestFile
inputFile="srl/python/SemanticRoleMiner/testCases/test2"
myTestFile=SenSta(inputFile)
myTestFile.makeSenna()
myTestFile.makeStanf()


#-- Test: PART1: getting info about sen0 from Senna and Stan ; generating labelels to each (Token,Token_Location)  
SEN0_SE=myTestFile.sennaDict['sen0']
SEN0_ST=myTestFile.stanfDict['sen0']
root=myTestFile.findRoot(SEN0_ST)
#print root
allPreds=findPreds(SEN0_SE)
#myTestFile.allPredicates=allPreds
#print allPreds

#---- testing predicates ------------
i=1
PRED={}
ARGS={}
for item in allPreds.values():
    verb=item[0][0]
    col=item[1]
    if verb==root:
       PRED[0]=verb
       ARGS[0]=findArg(root,SEN0_SE,col)
    else:
       PRED[i]=verb
       ARGS[i]=findArg(verb,SEN0_SE,col)
       i+=1 
print PRED
print ARGS


pred1=allPreds[0]
#print pred1
Col=pred1[1]
#print Col
rootArgs= findArg(root,SEN0_SE,Col)
#print rootArgs

pred0=allPreds[1]
Col=pred0[1]
pred0=pred0[0][0]
pred0Args= findArg(pred0,SEN0_SE,Col)
#print pred0Args
Preds={}
Preds[0]=root
Preds[1]=pred0

#print Preds
#print root,pred0

#-------------------------------------
# Domain of each arg
ARGDOM={}
for key,val in ARGS.items():
    #print key
    #print val
    ARGDOM[key]=findDomain(val)

rootArgDomain=findDomain(rootArgs)

pred0ArgDomain=findDomain(pred0Args)

ArgDomains={}
ArgDomains[0]=rootArgDomain
ArgDomains[1]=pred0ArgDomain

#print ArgDomains
#print ARGDOM[0]
#rootArgDomain
#------------------------------------

#-- Test: PART2: combining dependecy-relations with labels ; A1=[ partmod[ (Token1,loc1),(Token2,loc2)] , ....      ]
rootMixedArgs=mixDepArg(SEN0_ST,ARGS[0],PRED[0])
#print rootMixedArgs
pred0MixedArgs=mixDepArg(SEN0_ST,ARGS[1],PRED[1])
#print pred0MixedArgs

MixedArgs={}
MixedArgs[0]=rootMixedArgs
MixedArgs[1]=pred0MixedArgs


#print rootMixedArgs
#print "-----"
#for key,val in MixedArgs.items():
    #print key, val
#-----------------------------------
#-- Making relations
#print rootArgs

statement={}


rootSt0=makeSt0(root,rootArgs)
pred0St0=makeSt0(pred0,pred0Args)


predicates=[]
for key,val in allPreds.items():
    predicates.append(val[0][0])
#print pr

#-----------------------------------
#--verbDependencyArg
start=100
for key,verb in PRED.items():
	vda=verbDepArg(verb,MixedArgs[key],ArgDomains[key],predicates)
	fixSt0="St0-"+verb
	#print vda
	for tuples in vda.values():
	    test=fixSt0+" "+tuples[0].split("-")[0]+" "+tuples[0]
	    #print test
	    if test not in statement.values():
	       statement[str(start)]=test
	       start+=1
	    statement[str(start)]=tuples[0]+" "+tuples[1]+" "+tuples[2]
	    start+=1

#print statement
#-----------------------------------
#-- makeSubRelations


for key,verb in PRED.items():
    	#print key, p, MixedArgs[key]
	values=statement.values()
	newSts=makeSubSt(verb,MixedArgs[key],predicates,statement)
	for item in newSts.values():
	    thing=item[0]+" "+item[1]+" "+item[2] 
	    thing2=item[2]+" "+item[1]+" "+item[0]
	    if (thing not in values) and (thing2 not in values) and (item[0] not in predicates) and (item[2] not in predicates):
	      # print thing
	       statement[str(start)]=item[0]+" "+item[1]+" "+item[2]
	       start+=1

print statement

#---------------------------------------------
#-- visualization

#makeGephi(statement,inputFile)



