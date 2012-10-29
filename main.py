#importing SenSta class for creating 
from StanSennaClass import SenSta
from FindPropArg import findArg
from FindPropArg import findPreds
from FindPropArg import mixDepArg
from FindPropArg import findDomain
from CreateRelations import makeRel

#working with class object myTestFile
inputFile="~/srl/python/SemanticRoleMiner/testCases/test3/test_input.txt"
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

#-------------------------------------
# Domain of each arg
rootArgsDomain=findDomain(rootArgs)
#print rootArgsDomain
pred0ArgDomain=findDomain(pred0Args)
#print pred0ArgDomain

#------------------------------------

#-- Test: PART2: combining dependecy-relations with labels ; A1=[ partmod[ (Token1,loc1),(Token2,loc2)] , ....      ]
rootMixedArgs=mixDepArg(SEN0_ST,rootArgs,root)
print rootMixedArgs
pred0MixedArgs=mixDepArg(SEN0_ST,pred0Args,pred0)
print pred0MixedArgs

#-- Part3: Creating Relations by dependencies and args
#makeRel(mixedArgs,myTestFile.rootArgsDomain)




