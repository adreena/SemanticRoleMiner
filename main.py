#importing SenSta class for creating 
from StanSennaClass import SenSta
from FindPropArg import findArg
from FindPropArg import mixDepArg
from CreateRelations import makeRel

#working with class object myTestFile
inputFile="~/srl/python/SemanticRoleMiner/test/test_input1.txt"
myTestFile=SenSta(inputFile)
myTestFile.makeSenna()
myTestFile.makeStanf()


#-- Test: PART1: getting info about sen0 from Senna and Stan ; generating labels to each (Token,Token_Location)  
SEN0_SE=myTestFile.sennaDict['sen1']
SEN0_ST=myTestFile.stanfDict['sen1']
#print SEN0_ST['root']
args= findArg(SEN0_ST['root'],SEN0_SE)
#
#print SEN0_SE
#print "=-----------"
#print SEN0_ST
#print "------------"
#print args



#-- Test: PART2: combining dependecy-relations with labels ; A1=[ partmod[ (Token1,loc1),(Token2,loc2)] , ....      ]
mixedArgs=mixDepArg(SEN0_ST,args)
#print mixedArgs

#-- Part3: Creating Relations by dependencies and args
makeRel(mixedArgs)




