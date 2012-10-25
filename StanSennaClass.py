#for using terminal , calling senna and stanford parser
import os
from sennaProcessed import modifySenna
from stanfProcessed import modifyStanf

class SenSta:

   inputFile="Null"
   sennaOutFile="/home/kimia/srl/python/SemanticRoleMiner/test/senna"
   stanOutFile ="/home/kimia/srl/python/SemanticRoleMiner/test/stan"
   sennaDict={}
   stanfDict={}
   rootArgs={}
   rootArgsDomain={}
   otherPredicates={}
   def __init__(self,arg):
	self.inputFile=arg


   def makeSenna(self):
        #running senna to generate sennaoutput 
        cmd=os.system('cd /home/kimia/srl/senna \n ./senna <'+self.inputFile+'> '+self.sennaOutFile+'output1.txt')
        self.sennaDict=modifySenna(self.sennaOutFile+'output1.txt')
        return self.sennaDict 
  # output => {'sen2': {}, 
  #            'sen0':{
  #			1: {'Tanks': {1: 'NNS', 2: 'S-NP', 3: 'O', 4: '-', 5: 'S-A0', 6: 'B-A0', 7: '(S1(S(NP(NP*)'}}, 
  #			2: {'used': {1: 'VBN', 2: 'S-VP', 3: 'O', 4: 'used', 5: 'S-V', 6: 'I-A0', 7: '(VP*'}}, 
  #			3: {'for': {1: 'IN', 2: 'S-PP', 3: 'O', 4: '-', 5: 'B-A1', 6: 'I-A0', 7: '(PP*'}}, ... }
  #	       'sen1': {
  #                     1: {'Sand': {1: 'NN', 2: 'S-NP', 3: 'S-PER', 4: '-', 5: 'O', 6: 'O', 7: 'B-A1', 8: 'O', 9: 'O', 10: '(S1(S(NP*)'}}, 
  #			2: {'and': {1: 'CC', 2: 'O', 3: 'O', 4: '-', 5: 'O', 6: 'O', 7: 'I-A1', 8: 'O', 9: 'O', 10: '*'}}, .... }
  #            }                      

   def makeStanf(self):
        cmd=os.system('cd /home/kimia/srl/stanford-parser/ \n ./lexparser.sh '+self.inputFile+' >'+self.stanOutFile+'output1.txt')
        self.stanfDict=modifyStanf(self.stanOutFile+'output1.txt')
        return self.stanfDict

  # output => { 'sen0': {
  #			 0: 'nsubj(have-8, Tanks-1)', 
  #			 1: 'partmod(Tanks-1, used-2)', 
  #			 2: 'prep_for(used-2, storage-4)', 
  #			 3: 'nn(waters-7, process-6)', ... }
  #             'sen1': {
  #                    }





