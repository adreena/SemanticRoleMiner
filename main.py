#importing SenSta class for creating 
from StanSennaClass import SenSta

inputFile="~/srl/python/SemanticRoleMiner/test/test_input1.txt"
myTestFile=SenSta(inputFile)
myTestFile.makeSenna()
myTestFile.makeStanf()
print myTestFile.sennaDict
print myTestFile.stanfDict
