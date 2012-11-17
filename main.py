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
pred1=allPreds[1]
#print pred1
Col=pred1[1]
#print Col
root=pred1[0][0]
rootArgs= findArg(root,SEN0_SE,Col)
#print rootArgs

pred0=allPreds[0]
Col=pred0[1]
pred0=pred0[0][0]
pred0Args= findArg(pred0,SEN0_SE,Col)
#print pred0Args
Preds={}
Preds[0]=root
Preds[1]=pred0
#-------------------------------------
# Domain of each arg
rootArgDomain=findDomain(rootArgs)
#print rootArgsDomain
pred0ArgDomain=findDomain(pred0Args)
#print pred0ArgDomain
ArgDomains={}
ArgDomains[0]=rootArgDomain
ArgDomains[1]=pred0ArgDomain
#------------------------------------

#-- Test: PART2: combining dependecy-relations with labels ; A1=[ partmod[ (Token1,loc1),(Token2,loc2)] , ....      ]
rootMixedArgs=mixDepArg(SEN0_ST,rootArgs,root)
#print rootMixedArgs
pred0MixedArgs=mixDepArg(SEN0_ST,pred0Args,pred0)
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
for key,verb in Preds.items():
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


for key,verb in Preds.items():
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


