# Semantic Role Miner 

##                usign Stanford Parser , Senna

Senna is a SRL tool, receiving an input sentence , serving a set of tages for each token wihtin that sentence.
Output line include POS tag, Chunker tag, NER tag, SRL and corresponding Arg-tags for each predicate identified by SRL (a column for each) and tree.

complicated? here is an example:
sentence input : Tanks used for storage of process waters have apparent visible debris, filth, and microbiological contamination.
         
         output: token         POS        IOBE          NER             SRL       ARG           ARG               tree 
                 Tanks         NNS	      S-NP	   O	          -	 S-A0	      B-A0	(S1(S(NP(NP*)
                 used	    VBN	      S-VP	   O	         used	  S-V	      I-A0	(VP*
                 ...
           
Stanford parser serves us with a set of different information about each token:
         
         output:
                  nsubj(have-8, Tanks-1)
                  partmod(Tanks-1, used-2)
                  ...

My challenge is using both of these formats and creating meaningful triples (rdf) for further query purposes and building machine readable strucre out of them.
in other words, changing this sentence to machine interpretable format !

------------------------------------
  
 1- First Step:
 
  finding root predicate root(ROOT,verb) from stanford output. and finding its corresponding argmuments from Senna output.
  
  why root? root is main joint node , connecting all other nodes together, once the root of the sentence is found, main subject and object are targeted.
  
  We can then simplify subjects and objects, by means of separating their modifiers from them and describe them in triple forms.
  
  
to be continued...  