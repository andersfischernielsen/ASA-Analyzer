from datatypes import Analysis, CFGBranch, CFGNode, type_assignment, type_declaration, type_if, type_while, type_binary_operator, type_return, type_constant, type_variable
from pycparser import parse_file, c_parser, c_generator, c_ast

def convert_to_cfg(statements, next=None): 
    def get(compound, index):
        try:
            if hasattr(compound, 'block_items'): 
                return compound.block_items[index]
            else:
                return compound
        except IndexError:
            return next
    
    cfg = []
    for index, statement in enumerate(statements):
        if (isinstance(statement, c_ast.Constant)):
            cfg.append(CFGNode(type=type_constant, from_node=statement, to_node=get(statements, index+1), lvalue=statement.value))
        elif (isinstance(statement, c_ast.ID)):
            cfg.append(CFGNode(type=type_variable, from_node=statement, to_node=get(statements, index+1), lvalue=statement.name))
        elif (isinstance(statement, c_ast.Decl)):
            cfg.append(CFGNode(type=type_declaration, from_node=statement, to_node=get(statements, index+1), lvalue=statement.name))
        elif (isinstance(statement, c_ast.Assignment)):
            cfg.append(CFGNode(type=type_assignment, from_node=statement, to_node=get(statements, index+1), lvalue=statement.lvalue.name, rvalue=convert_to_cfg([statement.rvalue])[0]))
        elif (isinstance(statement, c_ast.BinaryOp)):
            cfg.append(CFGNode(type=type_binary_operator, from_node=statement, to_node=get(statements, index+1), lvalue=convert_to_cfg([statement.left])[0], rvalue=convert_to_cfg([statement.right])[0]))
        elif (isinstance(statement, c_ast.Return)):
            node = CFGNode(type=type_return, from_node=statement, to_node=get(statements, index+1), lvalue=None, rvalue=convert_to_cfg([statement.expr])[0])
            cfg.append(node)
        elif (isinstance(statement, c_ast.If)):
            if_true = convert_to_cfg(statement.iftrue, next=get(statements, index+1))
            if_false = convert_to_cfg(statement.iffalse, next=get(statements, index+1))
            if_branch = CFGBranch(type=type_if, from_node=statement, left=if_false, right=if_true)
            cfg.append(if_branch)
        elif (isinstance(statement, c_ast.While)):
            while_branch = CFGBranch(type=type_while, from_node=statement, left=convert_to_cfg(next), right=convert_to_cfg(statement.stmt, next=get(statements, index+1)))
            cfg.append(while_branch)
    return cfg

def convert_to_cfg_v2(statements: list):
    from collections import deque
    
    def is_statement(node):
        return False

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
            #we are in either the true or false branch
            #so to link the right nodes
            top.successors.append(current)
            if len(top.successors) != 2:
                #we are not finished linking top
                unlinked.appendleft(top)
            unlinked.appendleft(current)
            #Now here I'm not clear how to proceed... but the idea is:
            #lets say you have:
            # if(cond){stmt1;...stmt_j} else {stmt_i;...stmt_k}
            # so the stack would have: [cond] when you enter either branch.. 
            # so, when you see stmt1, you link stmt1 to cond and then, when you enter the else branch
            # you would link stmt_i to cond.
            # when you finish both branches.. you will have in the stack [stmt_j,stmt_k] and both need to be
            # linked to whatever comes next.. if nothing comes next (end of program) we add a new 'exit' node


def getAllExpressionsInProgram(cfg) -> list:
    return [""]

def getAllVariablesInProgram(cfg) -> set:
    variables = []
    for entry in cfg:
        if isinstance(entry, CFGNode) and entry.type == type_declaration:
            variables.append(entry.lvalue)
        if isinstance(entry, CFGBranch): 
            variables.extend(getAllVariablesInProgram(entry.left))
            variables.extend(getAllVariablesInProgram(entry.right))

    return set(variables)