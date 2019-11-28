import sys, os
from datatypes import Analysis, CFGBranch, CFGNode, type_assignment, type_declaration, type_if, type_while, type_binary_operator, type_return
from pycparser import parse_file, c_parser, c_generator, c_ast
from cfg import cfg as generator, cfg_nodes
from cfg_generator import convert_to_cfg
from fixpoint import find_fixpoint


def generate_CFG (path:str): 
    ast = parse_file(path)
    body = ast.ext[0].body
    cfg = convert_to_cfg(body)
    return cfg, ast

# TODO: Define applying fixpoint to CFG resulting in a program *)
def apply_fixpoint(fixpoint, ast, cfg, analysis) -> str: 
    generator = c_generator.CGenerator()
    pretty = generator.visit(ast)
    # TODO: Fix this based on new analysis types.
    stringified_elements = map(lambda n: str(n), cfg)
    zipped = list(map(lambda t: f"  {t[0]}, {t[1]},", zip(fixpoint, stringified_elements)))
    joined = str.join('\n', zipped)
    stringified = f"[\n{joined}\n]"

    return f"Got program: \n{pretty}\nFound fixpoint as:\n{stringified}"

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
    transformed = apply_fixpoint(fixpoint, ast, cfg, analysis)
    return transformed

def main():
    analyses = parse_analyses(sys.argv[1])
    path = sys.argv[2]
    for analysis in analyses:
        program = analyze(analysis, path)
    print(program)

if __name__ == "__main__":
    main()