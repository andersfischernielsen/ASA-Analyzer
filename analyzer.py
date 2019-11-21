import sys, os
from datatypes import Lattice, Analysis
from pycparser import parse_file, c_parser, c_generator, c_ast
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
        # TODO: This vector should be as long as the analysis steps in the CFG
        #       not the length of nodes in the CFG, so (steps in CFG) * 2 
        allVars = getAllVariablesInProgram(cfg)
        vector = dict(map(lambda v: (v, "bottom"), allVars))
        
        #TODO: Perform conjunction with the existing value during analysis. 
        for entry in cfg.get_entry_nodes():
            first = entry.get_func_first_node()
            ast = first.get_ast_elem_list()
            for node in ast:
                for t in transfer_functions:
                    res = t(node)
                    if res is not None: 
                        key = res[0] # TODO: Do conjunction here!
                        vector[key] = (res[1], node.coord.line)
        
        return vector

    # Recursively find the fixpoint
    def rec_apply(previous: list): 
        res = apply_transfer_functions(graph, cfg, transfer_functions)
        if res == previous:
            return res 
        else:
            return rec_apply(res)
    
    return rec_apply (apply_transfer_functions(graph, cfg, transfer_functions))

def getAllExpressionsInProgram(cfg) -> list:
    return [""]

def getAllVariablesInProgram(cfg) -> set:
    variables = []
    for entry in cfg.get_entry_nodes():
            first = entry.get_func_first_node()
            ast = first.get_ast_elem_list()
            for node in ast:
                if isinstance(node, c_ast.Decl):
                    variables.append(node.name)

    return set(variables)


# TODO: Define applying fixpoint to CFG resulting in a program *)
def apply_fixpoint(fixpoint, cfg, analysis) -> str: 
    ast = cfg.get_ast()

    generator = c_generator.CGenerator()
    pretty = generator.visit(ast)
    transformed = []

    for line_no, line in enumerate(pretty.splitlines(), start=1):
        for match in filter(lambda v: line_no == v[1], fixpoint.values()):
            line = f"{line}\t/* {analysis.lattice.symbols[match[0]]} */"
        
        transformed.append(line)
    
    return str.join('\n', transformed)

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
    transformed = apply_fixpoint(fixpoint, cfg, analysis)
    return transformed

def main():
    analyses = parse_analyses(sys.argv[1])
    path = sys.argv[2]
    for analysis in analyses:
        program = analyze(analysis, path)
    print(program)

if __name__ == "__main__":
    main()