#importing SenSta class for creating 
from StanSennaClass import SenSta
from FindPropArg import findArg
from FindPropArg import findPreds
from FindPropArg import mixDepArg
from FindPropArg import findDomain
from CreateRelations import makeRel

#working with class object myTestFile
inputFile="~/srl/python/SemanticRoleMiner/testCases/test1/test_input1.txt"
myTestFile=SenSta(inputFile)
myTestFile.makeSenna()
myTestFile.makeStanf()


#-- Test: PART1: getting info about sen0 from Senna and Stan ; generating labelels to each (Token,Token_Location)  
SEN0_SE=myTestFile.sennaDict['sen0']
SEN0_ST=myTestFile.stanfDict['sen0']
#print SEN0_ST['root']
rootArgs= findArg(SEN0_ST['root'],SEN0_SE)
myTestFile.rootArgs=rootArgs

otherPreds=findPreds(SEN0_SE)

#print myTestFile.rootArgs
#
#print "SENNA DICTIONARY:\n"+str(SEN0_SE)
#print "=-----------"
#print "STANFORD DICTIONARY:\n"+str(SEN0_ST)
#print "------------"
#print "SENNA ARG LABELS:\n"+str(args)
 
# domain of each arg
#myTestFile.rootArgsDomain=findDomain(args)
#print myTestFile.argDomains

#-- Test: PART2: combining dependecy-relations with labels ; A1=[ partmod[ (Token1,loc1),(Token2,loc2)] , ....      ]
#mixedArgs=mixDepArg(SEN0_ST,args)
#print mixedArgs

#-- Part3: Creating Relations by dependencies and args
#makeRel(mixedArgs,myTestFile.rootArgsDomain)




