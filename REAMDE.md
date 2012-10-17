# Semantic Role Miner usign Stanford Parser , Senna

Senna is a SRL tool, receiving an input sentence , serving a set of tages for each token wihtin that sentence.
Output line include POS tag, Chunker tag, NER tag, SRL and corresponding Arg-tags for each predicate identified by SRL (a column for each) and tree.

complicated? here is an example:
sentence input : Tanks used for storage of process waters have apparent visible debris, filth, and microbiological contamination.
         
         output: token         POS        IOBE          NER             SRL       ARG         ARG   tree 
                 Tanks         NNS	      S-NP	         O	              -	      S-A0	      B-A0	(S1(S(NP(NP*)
                 used	         VBN	      S-VP	         O	           used	       S-V	      I-A0	(VP*