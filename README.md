***
ASA Analyzer
*** 

A code analyzer for a subset of C. 

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

## Running
The analyzer is run by executing the main script and providing a comma-separated list of which analyses to run on a given file. 

Analyses must be implemented and be present in the `analyzers` folder of the project, otherwise an error will be raised. 
