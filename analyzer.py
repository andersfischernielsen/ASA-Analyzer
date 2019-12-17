import sys
import os
from datatypes import Analysis, CFGBranch, CFGNode, type_assignment, type_declaration, type_if, type_while, type_binary_operator, type_return
from pycparser import parse_file, c_parser, c_generator, c_ast
from controlflow import convert_to_cfg, print_cfg, get_expressions_in_program, get_variables_in_program, \
    cfg_to_list, from_node_fixer, to_node_to_succ, add_entry_exit_nodes, get_expressions_in_program,\
    get_variables_in_program
from fixpoint import find_fixpoint


def generate_CFG(path: str):
    ast = parse_file(path)
    body = ast.ext[0].body
    cfg = convert_to_cfg(body)
    cfg_l = cfg_to_list(cfg)
    from_node_fixer(cfg_l)
    cfg = add_entry_exit_nodes(cfg_l)
    # this is ugly but... :(
    cfg_l = cfg_to_list(cfg)
    to_node_to_succ(cfg_l)
    return cfg, ast

# TODO: Define applying fixpoint to CFG resulting in a program *)


def apply_fixpoint(fixpoint, ast, cfg, analysis) -> str:
    generator = c_generator.CGenerator()
    original = generator.visit(ast)
    with_information = generator.visit(ast).split('\n')
    ast_with_current_nodes = list(
        filter(lambda n: n[0].current_node, fixpoint))
    for node in ast_with_current_nodes:
        index = node[0].current_node.coord.line-1
        line = with_information[index]
        with_information[index] = line + f' /* {node[1]} */'
    return original, '\n'.join(with_information)


def parse_analyses(input: str) -> [Analysis]:
    analyses = input.split(':')
    lst = os.listdir("analyzers")
    res = {}

    analysis_directories = []
    for directory in lst:
        s = os.path.abspath("analyzers") + os.sep + directory
        if os.path.isdir(s) and os.path.exists(s + os.sep + "__init__.py"):
            analysis_directories.append(directory)

    for directory in analysis_directories:
        if (directory in analyses):
            res[directory] = __import__(
                "analyzers." + directory, fromlist=["*"]).analysis

    return list(res.values())


def analyze(analysis: Analysis, path: str) -> str:
    cfg, ast = generate_CFG(path)
    cfgl = cfg_to_list(cfg)
    # Initialization of expressions, variables and state
    # of the analysis
    analysis.expressions = get_expressions_in_program(cfgl)
    analysis.variables = get_variables_in_program(cfgl)
    analysis.init_state(cfgl)
    fixpoint = find_fixpoint(analysis)
    program, transformed = apply_fixpoint(fixpoint, ast, cfg, analysis)
    return f"Got program: \n{program}\nFound fixpoint as:\n{transformed}"


def main():
    analyses = parse_analyses(sys.argv[1])
    path = sys.argv[2]
    for analysis in analyses:
        output = analyze(analysis, path)
    print(output)


if __name__ == "__main__":
    main()
