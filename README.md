SemanticRoleMiner
=================

Turning a text into Graph

Introduction
----

Natural Language Processing (NLP) has been a key to variety of language-oriented tasks including 
<strong>query answering engines , text summarization tools, event detection systems,</strong> and many other tools that deal with human written textual documents.
Such tasks require deep understanding of the underlying structures and semantics of the text. 
On the other hand, Ontology provides a framework for representing extracted information, 
in the format of entities and relationships among them. 
This framework is machine-readable and allows sharing and exchanging of knowledge between different applications.
Most of the tools designed for discussed purposes are not successful to cover all aspects of linguistic analysis for texts. Query engines and ontology learners such as BIEQA, Text2Onto and OntoPlus rely on bag-of-words and pattern-matching methods, which also make them domain-specific and user-dependent. FRED mines more information from texts in terms of semantic-roles and relations between terms.
Meanwhile, a big portion of its output is unnecessary and the size of output can be reduced by merging and more analysis.  


Building Blocks
---
Stanford parser is a statistical NLP tool, written in Java, for generating grammatical structure of a raw text. 
This system is able to check over 50 grammatical relations and produces different formats of outputs
and linguistic analysis. It is trained on the Penn Wall Street Journal Treebank and supports many languages such as 
English, Chinese, German, Arabic and French. Output contains different levels of dependency graphs and trees for 
various purposes.
From a general point of view, Stanford parser splits the sentence into two parts, root, or verb, and dependents. 
Grammatical relations go under the category of dependents. 
Parser discovers phrasal structures in the text and their relation to root. 
Each phrase is also studied individually for identifying head-word and its modifiers such as temporal, 
possessive and relative clause modifiers. When parser is not able to find any matches for a relation, leaves it as a dependent. 
Stanford specification:
Semantic/Syntactic Extraction using a Neural Network Architecture (Senna) 
creates several layers of features exploited from unlabelled data, using neural network techniques. 
Neural network is an adaptive system for real-world problem solving. Each layer provides a basis for other 
layers and makes the approach almost independent from anyprior knowledge. Because of following a neural network structure, 
Senna does all text analysis from scratch.
Senna follows PropBank annotation style for semantic role labelling. 
PropBank annotators examine instances from their databank and decide which frameset suits the given sentence the best. 
In some cases, annotator has to decide between two roles for a word.
They often apply ranking strategy of Arg0 > Arg1 > Arg2 >… to make the final decision.

We formulate procedure of creating RDF triples into four steps: 

	Pre-processing
	
	Simplification 
	
	Generating Triples 
	
	Representation.  

 
 
 Sample input and output
 ---
 Example 1:
 
 	Input: "Farmers with salmonella in the herd should advise Fonterra [multinational dairy company]", he said.
 	
 	output: [graph]: http://i44.tinypic.com/207us02.jpg
 
 	
 
 
 
