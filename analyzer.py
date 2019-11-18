import sys, os
from datatypes import Lattice, Analysis

# TODO: Define directed graph structure
graph = []

# TODO: Define graph parsing *)
def generate_graph(lattice:Lattice) -> int:
    return 0

def generate_CFG (path:str): 
    from pycparser import parse_file
    from cfg import cfg

    graph = cfg.CFG(path)
    cfg = graph.make_cfg()
    return cfg

def find_fixpoint(graph, ast, transfer_functions) -> [str]:
    # TODO: Define finding fixpoint
    def apply_transfer_functions(graph, ast, transfer_functions) -> [str]:
        return [""]

    # Recursively find the fixpoint
    def rec_apply(previous: list): 
        res = apply_transfer_functions(graph, ast, transfer_functions)
        if res == previous:
            return res 
        else:
            return rec_apply(res)
    
    rec_apply (apply_transfer_functions(graph, ast, transfer_functions))

def getAllExpressionsInProgram(input: str) -> list:
    return [""]

def getAllVariablesInProgram(input: str) -> list:
    return [""]

# TODO: Define applying fixpoint to AST resulting in a program *)
def apply_fixpoint(fixpoint, ast) -> str: 
    return ""

# TODO: Define pretty-printing of AST application - might not be needed *)
def pretty_print(transformed_program) -> str:
    return transformed_program

def parse_analyses (input:str) -> [Analysis]:
    analyses = input.split(':')
    res = {}
    lst = os.listdir("analyzers")
    
    dir = []
    for d in lst:
        s = os.path.abspath("analyzers") + os.sep + d
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            dir.append(d)
    
    for d in dir:
        if (d in analyses):
            res[d] = __import__("analyzers." + d, fromlist = ["*"])
    
    return list(res.values())

def analyze (analysis:Analysis, path:str) -> str:
    graph = generate_graph(analysis)
    cfg = generate_CFG(path)
    fixpoint = find_fixpoint(graph, cfg, analysis)
    transformed = apply_fixpoint(fixpoint, cfg)
    pretty = pretty_print(transformed)
    return pretty

def main():
    analyses = parse_analyses(sys.argv[1])
    path = sys.argv[2]
    for analysis in analyses:
        program = analyze(analysis, path)
    print(program)

if __name__ == "__main__":
    main()