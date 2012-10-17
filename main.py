#importing SenSta class for creating 
from StanSennaClass import SenSta

inputFile="~/srl/python/SemanticRoleMiner/test/test_input1.txt"
myTestFile=SenSta(inputFile)
print myTestFile.getSennaOutput()
print myTestFile.getStanOutput()
