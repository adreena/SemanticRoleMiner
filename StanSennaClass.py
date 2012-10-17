#for using terminal , calling senna and stanford parser
import os


class SenSta:

   inputFile="Null"
   sennaOutFile="~/srl/python/SemanticRoleMiner/test/senna"
   stanOutFile ="~/srl/python/SemanticRoleMiner/test/stan"
   def __init__(self,arg):
	self.inputFile=arg

   def getSennaOutput(self):
        #running senna to generate sennaoutput 
        cmd=os.system('cd /home/kimia/srl/senna \n ./senna <'+self.inputFile+'> '+self.sennaOutFile+'output1.txt')
        return self.inputFile+" Senna Here" 

   def getStanOutput(self):
        cmd=os.system('cd /home/kimia/srl/stanford-parser/ \n ./lexparser.sh '+self.inputFile+' >'+self.stanOutFile+'output1.txt')
        return self.inputFile+" Stan Here"


