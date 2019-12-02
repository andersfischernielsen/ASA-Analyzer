***
ASA Analyzer
*** 

A code analyzer for a subset of C. 

## Requirements
- [x] General analysis interface must be present
	- [ ] User can supply own lattice
	- [ ] User can supply own transfer functions 
- [ ] May/must should be implemented (forwards-backwards)
- [ ] Start with lock/unlock
- [ ] Combine several lattice structures (analyses) to make analysis smarter
- [ ] Optionally insert program repair for missing unlocks

## Program Flow
- User provides 
  - a lattice,
  - a list of transfer functions, 
  - an input program
- Analysis is performed until a fixpoint is found
- Analysis is applied to CFG
- An output program based on the transformed CFG is generated
- User gets an analysed & annotated program as output

### Structure of analysis
```
Program         -> CIL-CFG          -> Analysis vector                 -> CIL-CFG      -> Program
Original source -> Get CFG from CIL -> Apply transfer functions           Pretty print
                                       by use of lattice
                                       resulting in a fixpoint vector
                                       which is applied onto the CFG
                                       resulting in an "optimized" CFG
```