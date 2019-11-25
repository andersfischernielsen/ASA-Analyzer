import sys, os
from datatypes import Analysis, CFGBranch, CFGNode, type_assignment, type_declaration, type_if, type_while, type_binary_operator, type_return
from pycparser import parse_file, c_parser, c_generator, c_ast
from cfg import cfg as generator, cfg_nodes


# TODO: Implement recursive CFG generation.
def convert_to_cfg(statements): 
    def get(compound, index):
        try:
            return compound.block_items[index]
        except IndexError:
            return None
    
    cfg = []
    for index, statement in enumerate(statements):
        if (isinstance(statement, c_ast.Decl)):
            cfg.append(CFGNode(type=type_declaration, from_node=statement, to_node=get(statements, index+1), lvalue=statement.name))
        elif (isinstance(statement, c_ast.Assignment)):
            cfg.append(CFGNode(type=type_assignment, from_node=statement, to_node=get(statements, index+1), lvalue=statement.lvalue.name, rvalue=statement.rvalue.value))
        elif (isinstance(statement, c_ast.BinaryOp)):
            cfg.append(CFGNode(type=type_binary_operator, from_node=statement, to_node=get(statements, index+1)))
        elif (isinstance(statement, c_ast.Return)):
            cfg.append(CFGNode(type=type_return, from_node=statement, to_node=get(statements, index+1)))
        elif (isinstance(statement, c_ast.If)):
            if_true = convert_to_cfg(statement.iftrue)
            if_false = convert_to_cfg(statement.iffalse)
            if_false[-1].to_node = to_node=get(statements, index+1)
            if_true[-1].to_node = to_node=get(statements, index+1)
            if_branch = CFGBranch(type=type_if, from_node=statement, left=if_false, right=if_true)
            cfg.append(if_branch)
        elif (isinstance(statement, c_ast.While)):
            while_branch = CFGBranch(type=type_while, left=get(statements, index+1), right=convert_to_cfg(statement.stmt))
            cfg.append(while_branch)
    return cfg

def generate_CFG (path:str): 
    ast = parse_file(path)
    body = ast.ext[0].body
    cfg = convert_to_cfg(body)
    return cfg, ast

def find_fixpoint(cfg, transfer_functions) -> {}:
    def apply_transfer_functions(cfg, transfer_functions) -> {}:
        # TODO: This vector should be as long as the analysis steps in the CFG
        #       not the length of nodes in the CFG, so (steps in CFG) * 2 
        allVars = getAllVariablesInProgram(cfg)
        tuples = []
        for i in range(0, len(cfg)):
            tuples.append((i, ("bottom", 0)))
        vector = dict(tuples)

        #TODO: Perform conjunction with the existing value during analysis. 
        for i, entry in enumerate(cfg):
            for t in transfer_functions:
                res = t(entry)
                if res is not None: 
                    vector[i] = (res[1], entry.coord.line) # TODO: Do conjunction here!
                else: 
                    vector[i] = (vector[i][0], entry.coord.line)
        
        return vector

    # Recursively find the fixpoint
    def rec_apply(previous: list): 
        res = apply_transfer_functions(cfg, transfer_functions)
        if res == previous:
            return res 
        else:
            return rec_apply(res)
    
    return rec_apply (apply_transfer_functions(cfg, transfer_functions))

def getAllExpressionsInProgram(cfg) -> list:
    return [""]

def getAllVariablesInProgram(cfg) -> set:
    variables = []
    # TODO: Implement to match new types in CFG.
    # for entry in cfg:
    #     if isinstance(entry, c_ast.Decl):
    #         variables.append(entry.name)

    return set(variables)


# TODO: Define applying fixpoint to CFG resulting in a program *)
def apply_fixpoint(fixpoint, ast, analysis) -> str: 
    generator = c_generator.CGenerator()
    pretty = generator.visit(ast)
    transformed = []

    # TODO: Fix this based on new analysis types.
    # for line_no, line in enumerate(pretty.splitlines(), start=1):
    #     for match in filter(lambda v: line_no == v[1], fixpoint.values()):
    #         line = f"{line}\t/* {analysis.lattice.symbols[match[0]]} */"
        
    #     transformed.append(line)
    
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
    cfg, ast = generate_CFG(path)
    fixpoint = find_fixpoint(cfg, analysis.transfer_functions)
    transformed = apply_fixpoint(fixpoint, ast, analysis)
    return transformed

def main():
    analyses = parse_analyses(sys.argv[1])
    path = sys.argv[2]
    for analysis in analyses:
        program = analyze(analysis, path)
    print(program)

if __name__ == "__main__":
    main()