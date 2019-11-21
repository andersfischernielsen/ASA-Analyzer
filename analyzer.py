import sys, os
from datatypes import Lattice, Analysis
from pycparser import parse_file, c_parser, c_generator
from cfg import cfg as generator, cfg_nodes

# TODO: Define graph parsing *)
def generate_graph(lattice:Lattice) -> int:
    return 0

def generate_CFG (path:str): 
    graph = generator.CFG(path)
    graph.make_cfg()
    return graph

def find_fixpoint(graph, cfg, transfer_functions) -> {}:
    def apply_transfer_functions(graph, cfg, transfer_functions) -> {}:
        vector = {}
        
        for entry in cfg.get_entry_nodes():
            first = entry.get_func_first_node()
            ast = first.get_ast_elem_list()
            for node in ast:
                for t in transfer_functions:
                    vector = t(vector, node)
        
        return vector

    # Recursively find the fixpoint
    def rec_apply(previous: list): 
        res = apply_transfer_functions(graph, cfg, transfer_functions)
        if res == previous:
            return res 
        else:
            return rec_apply(res)
    
    return rec_apply (apply_transfer_functions(graph, cfg, transfer_functions))

def getAllExpressionsInProgram(input: str) -> list:
    return [""]

def getAllVariablesInProgram(input: str) -> list:
    return [""]

# TODO: Define applying fixpoint to CFG resulting in a program *)
def apply_fixpoint(fixpoint, cfg): 
    return

# TODO: Define pretty-printing of CFG application - might not be needed *)
def pretty_print(transformed_program) -> str:
    generator = c_generator.CGenerator()
    return generator.visit(transformed_program)

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
            res[d] = __import__("analyzers." + d, fromlist = ["*"]).analysis
    
    return list(res.values())

def analyze (analysis:Analysis, path:str) -> str:
    graph = generate_graph(analysis)
    cfg = generate_CFG(path)
    fixpoint = find_fixpoint(graph, cfg, analysis.transfer_functions)
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