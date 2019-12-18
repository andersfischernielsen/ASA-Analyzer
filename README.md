***
ASA Analyzer
*** 

A code analyzer for a subset of C. 

## Running
The analyzer is run by executing the main script and providing a comma-separated list of which analyses to run on a given file, e.g. 

```
./analyzer.py busy_expressions:available_expressions example_files/example3.c
```

Analyses must be implemented and be present in the `analyzers` folder of the project, otherwise an error will be raised. 

### Using Docker
The analyzer can be run using Docker by building the Dockerfile: 
```
cd ASA-Analyzer/
docker build -f Dockerfile -t asa-analyzer
```

The image can then be launched by executing:
```
docker run -it asa-analyzer sh
```

The analyses can then be run by executing: 
```
./analyzer.py busy_expressions:available_expressions example_files/example3.c
```

## Program Flow
- The user provides 
  - a lattice,
  - a list of transfer functions, 
  - an input program
- The analysis is performed until a fixpoint is found
- The analysis is applied to CFG
- A program based on the transformed CFG is generated and presented

### Structure of analysis
```
   ←----------------------------------------------------------------------------------------
  ↓                                                                                         ↑
Program         -> CIL-CFG          -> Analysis vector                 -> CIL-CFG      -> Program
Input source    -> Get CFG from CIL -> Apply transfer functions        -> Pretty print -> Output 
                                       by use of lattice
                                       resulting in a fixpoint vector
                                       which is applied onto the CFG
                                       resulting in an "optimized" CFG
```
