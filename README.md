***
ASA Analyzer
*** 

A code analyzer for a subset of C. 

## Requirements
- General lattice interface must be present
- General transfer function interface must be present
- May/must should be implemented (forwards-backwards)
- Start with lock/unlock
- Combine several lattice structures (analyses) to make analysis smarter
- Optionally insert program repair for missing unlocks

## Program Flow
- User provides 
  - a set of lattice nodes, 
  - a function defining the partial ordering of the lattice, 
  - a list of transfer functions, 
  - and an input program
- We generate an ordered graph based on the product of the given "user set" and the ordering
- We then do BFS on this graph followed by set intersection of visited nodes, in order to determine the conjunction for two given nodes in the graph
- Do analysis until a fixpoint is found
- Apply analysis to CFG
- Generate output program based on CFG
- User gets a output program


### Structure of analysis
```
Program         -> CIL-CFG          -> Analysis vector                 -> CIL-CFG      -> Program
Original source -> Get CFG from CIL -> Apply transfer functions           Pretty print
                                       by use of lattice
                                       resulting in a fixpoint vector
                                       which is applied onto the CFG
                                       resulting in an "optimized" CFG
```

## Report
- Technical overview
- Evaluation
	- What can it do? 
	- What can it not do? 
