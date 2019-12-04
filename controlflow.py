from datatypes import *
from pycparser import parse_file, c_parser, c_generator, c_ast
from collections import deque

def convert_to_cfg(statements: list):
    raise NotImplementedError()    
    
    def is_statement(node):
        return node.type in [type_if, type_while, type_return]

    unlinked = deque()
    remaining = deque(statements)
    while len(remaining) > 0:
        current = remaining.popleft()
        top = unlinked.popleft()
        if not is_statement(top):
            top.successors = [current]
            unlinked.appendleft(current)
            continue
        if is_statement(top):
            #we are in either the true or false branch, link the right nodes
            top.successors.append(current)
            if len(top.successors) != 2:
                #we are not finished linking top
                unlinked.appendleft(top)
            unlinked.appendleft(current)
            # Now here I'm not clear how to proceed... but the idea is:
            # lets say you have:
            # if (cond) { stmt1;...stmt_j } 
            # else { stmt_i;...stmt_k }
            # so the stack would have: [cond] when you enter either branch.. 
            # so, when you see stmt1, you link stmt1 to cond and then, when you enter the else branch
            # you would link stmt_i to cond.
            # when you finish both branches.. you will have in the stack [stmt_j,stmt_k] and both need to be
            # linked to whatever comes next.. if nothing comes next (end of program) we add a new 'exit' node


def getAllExpressionsInProgram(cfg) -> list:
    raise NotImplementedError()
    return [""]

def getAllVariablesInProgram(cfg) -> set:
    raise NotImplementedError()
    return set()