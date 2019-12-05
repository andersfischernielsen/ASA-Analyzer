from datatypes import Analysis, CFGBranch, CFGNode, type_assignment, type_declaration, type_if, type_while, type_binary_operator, type_return, type_constant, type_variable
from pycparser import parse_file, c_parser, c_generator, c_ast

def convert_to_cfg(statements): 
    def get(list, index):
        if (index > len(list)-1): 
            return None
        if (index < 0): 
            return None
        try:
            return list[index]
        except IndexError:
            return None

    def link(l):
        for i in range(0, len(l)-1): 
            get(l, i).to_node = get(l, i+1)
            get(l, i).from_node = get(l, i-1)

    def parse_node(statement, next=None):
        if (isinstance(statement, c_ast.Constant)):
            return CFGNode(type=type_constant, current_node=statement, lvalue=statement.value)
        elif (isinstance(statement, c_ast.ID)):
            return CFGNode(type=type_variable, current_node=statement, lvalue=statement.name)
        elif (isinstance(statement, c_ast.Decl)):
            return CFGNode(type=type_declaration, current_node=statement, lvalue=statement.name)
        elif (isinstance(statement, c_ast.Assignment)):
            return CFGNode(type=type_assignment, current_node=statement, lvalue=statement.lvalue.name, rvalue=parse_node(statement.rvalue))
        elif (isinstance(statement, c_ast.BinaryOp)):
            return CFGNode(type=type_binary_operator, current_node=statement, lvalue=statement.left.value, rvalue=statement.right.value)
        elif (isinstance(statement, c_ast.Return)):
            node = CFGNode(type=type_return, current_node=statement, lvalue=None, rvalue=statement.expr)
            return node
        elif (isinstance(statement, c_ast.If)):
            if_true = list(map(lambda s: parse_node(s, next=next), statement.iftrue))
            if_false = list(map(lambda s: parse_node(s, next=next), statement.iffalse))
            link(if_true)
            link(if_false)
            if_true[-1].to_node = next
            if_false[-1].to_node = next
            if_branch = CFGBranch(type=type_if, current_node=statement, true=if_true[0], false=if_false[0])
            if_branch.true.from_node = if_branch
            if_branch.false.from_node = if_branch
            return if_branch
        elif (isinstance(statement, c_ast.While)):
            if_true = list(map(lambda s: parse_node(s, next=next), statement.stmt))
            link(if_true)
            while_branch = CFGBranch(type=type_while, current_node=statement, true=if_true[0], false=next)
            while_branch.true.to_node = while_branch
            return while_branch
        return None

    if hasattr(statements, "block_items"):
        statements = statements.block_items

    parsed = [None] * len(statements)
    for index in range(0, len(statements)-1):
        prev = get(parsed, index-1)
        next = parse_node(get(statements, index+1))
        current = parse_node(get(statements, index), next=next)
            
        if prev: 
            prev.to_node = current
            parsed[index-1] = prev
        if next: 
            next.from_node = current
            parsed[index+1] = prev
        
        current.to_node = next
        current.from_node = prev
        parsed[index] = current

    return parsed[0]

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