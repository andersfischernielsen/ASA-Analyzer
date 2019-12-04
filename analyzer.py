import sys, os
from datatypes import *
from pycparser import parse_file, c_parser, c_generator, c_ast
from controlflow import convert_to_cfg
from fixpoint import find_fixpoint


def generate_CFG (path:str): 
    ast = parse_file(path)
    body = ast.ext[0].body
    cfg = convert_to_cfg(body)
    return cfg, ast

# TODO: Define applying fixpoint to CFG resulting in a program *)
def apply_fixpoint(fixpoint, cfg, ast) -> str: 
    if (ast):
        pretty = c_generator.CGenerator().visit(ast)
    else: 
        pretty = ""

    # TODO: Fix this based on new analysis types.
    stringified_elements = map(lambda n: str(n), cfg)
    zipped = list(map(lambda t: f"  {t[0]}, {t[1]},", zip(fixpoint, stringified_elements)))
    joined = str.join('\n', zipped)
    stringified = f"[\n{joined}\n]"
    return pretty, stringified

def get_analyses (input:str) -> [Analysis]:
    analyses = input.split(':')
    directories = os.listdir("analyzers")

    analysis_directories = []
    for directory in directories:
        s = os.path.abspath("analyzers") + os.sep + directory
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            analysis_directories.append(directory)
    
    res = {}
    for directory in analysis_directories:
        if (directory in analyses):
            res[directory] = __import__("analyzers." + directory, fromlist = ["*"]).analysis
    
    return list(res.values())

def analyze (analysis:Analysis, path:str) -> str:
    # TODO: Add back when CFG is implemented.
    # cfg, ast = generate_CFG(path)

    nodes = []
    nodes.append(CFGNode(0, frozenset(['x']), [],[1],[],'decl'))
    nodes.append(CFGNode(1, frozenset(['y']), [],[2],[0],'decl'))
    nodes.append(CFGNode(2, frozenset(['z']), [],[3],[1],'decl'))
    nodes.append(CFGNode(3, frozenset(['x']), [],[4],[2],'assignment'))
    nodes.append(CFGNode(4, frozenset(), ['>','x','1'],[5,12],[11],'cond'))
    nodes.append(CFGNode(5, frozenset(['y']),['/','x','2'],[6],[4],'assignment'))
    nodes.append(CFGNode(6, frozenset(), ['>','y','3'],[7,8],[5],'cond'))
    nodes.append(CFGNode(7, frozenset(['x']), ['-','x','y'],[6],[8],'assignment'))
    nodes.append(CFGNode(8, frozenset(['z']), ['-','x','4'],[9],[6,7],'assignment'))
    nodes.append(CFGNode(9, frozenset(), ['>','z','0'],[10,11],[8],'cond'))
    nodes.append(CFGNode(10, frozenset(['x']),['/','x','2'],[9],[11],'assignment'))
    nodes.append(CFGNode(11, frozenset(['z']), ['-','z','1'],[4],[9,10],'assignment'))
    nodes.append(CFGNode(12, frozenset(),['x'],[13],[4],'output'))
    nodes.append(CFGNode(13, frozenset(),[],[],[12],'exit'))
    cfg = CFG(nodes)

    fixpoint = find_fixpoint(cfg, analysis.transfer_functions)
    program, transformed = apply_fixpoint(fixpoint, cfg, None)
    return f"Got program: \n{program}\nFound fixpoint as:\n{transformed}"

def main():
    analyses = get_analyses(sys.argv[1])
    path = sys.argv[2]
    for analysis in analyses:
        output = analyze(analysis, path)
    print(output)


if __name__ == "__main__":
    main()