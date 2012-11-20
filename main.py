#importing SenSta class for creating 
from StanSennaClass import SenSta
from FindPropArg import Find_Pred_Arg_Root
from FindPropArg import Find_ArgDom_MixArgDep
from CreateRelations import makeStatements
from Visualizer import makeGephi


#working with class object myTestFile
inputFile="srl/python/SemanticRoleMiner/testCases/test1"
myTestFile=SenSta(inputFile)
myTestFile.makeSenna()
myTestFile.makeStanf()
SEN0_SE=myTestFile.sennaDict['sen0']
SEN0_ST=myTestFile.stanfDict['sen0']

#------------------------------------
# Find Predicates,root, and all Args for each predicate
PAR=Find_Pred_Arg_Root(myTestFile,SEN0_SE,SEN0_ST)
PRED=PAR[0]
ARGS=PAR[1]
root=PAR[2]

#-------------------------------------
# Find domain of each predicate and group all dependencies under each Args

AM=Find_ArgDom_MixArgDep(ARGS,PRED,SEN0_ST)
ARGDOM=AM[0]
MIXARGS=AM[1]


#-----------------------------------
# manipulating all statements 

statement=makeStatements(PRED,ARGDOM,MIXARGS)
print statement

#---------------------------------------------
#-- visualization

#makeGephi(statement,inputFile)



