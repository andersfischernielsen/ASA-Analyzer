from datatypes import Analysis, CFGBranch, CFGNode, type_assignment, type_declaration, \
    type_if, type_while, type_binary_operator, type_return, type_constant, type_variable,\
    type_entry, type_exit, type_output, type_input
from pycparser import parse_file, c_parser, c_generator, c_ast
import queue


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
        # Link all nodes with their predecessor and successor.
        for i in range(0, len(l)-1):
            current = get(l, i)
            current.to_node = get(l, i+1)
            current.from_node = get(l, i-1)
            if isinstance(current, CFGBranch):
                # Single-line if-statements need special care to preserve their false-branch.
                if not current.false:
                    current.false = get(l, i+1)
                if not current.false.from_node:
                    current.false.from_node = current

    def parse_node(statement, next=None):
        if (isinstance(statement, c_ast.Constant)):
            return CFGNode(type=type_constant, current_node=statement, lvalue=statement.value)
        if (isinstance(statement, c_ast.ID)):
            return CFGNode(type=type_variable, current_node=statement, lvalue=statement.name)
        if (isinstance(statement, c_ast.Decl)):
            return CFGNode(type=type_declaration, current_node=statement, lvalue=statement.name)
        if (isinstance(statement, c_ast.BinaryOp)):
            return CFGNode(type=type_binary_operator, current_node=statement,
                           lvalue=parse_node(statement.left), rvalue=parse_node(statement.right))
        if (isinstance(statement, c_ast.Return)):
            node = CFGNode(type=type_return, current_node=statement,
                           lvalue=None, rvalue=statement.expr)
            return node
        if (isinstance(statement, c_ast.Assignment)):
            # Normal assignments
            if (not isinstance(statement.rvalue, c_ast.FuncCall)):
                return CFGNode(type=type_assignment, current_node=statement,
                               lvalue=statement.lvalue.name, rvalue=parse_node(statement.rvalue))
            # Assignments to input()
            if (isinstance(statement.rvalue, c_ast.FuncCall) and
                    hasattr(statement.rvalue.name, "name") and statement.rvalue.name.name == "input"):
                return CFGNode(type=type_input, current_node=statement,
                               lvalue=statement.lvalue.name, rvalue="input")
        if (isinstance(statement, c_ast.If)):
            if_true = [parse_node(statement.iftrue, next=next)] if not statement.iffalse else \
                list(map(lambda s: parse_node(s, next=next),
                         statement.iftrue)) if statement.iftrue else []
            if_false = list(map(lambda s: parse_node(s, next=next),
                                statement.iffalse)) if statement.iffalse else []
            link(if_true)
            link(if_false)
            # Make the last true node point to the next statement in the CFG.
            if if_true:
                if_true[-1].to_node = next
            # Same goes for the last false node.
            if if_false:
                if_false[-1].to_node = next
            if_branch = CFGBranch(type=type_if, current_node=statement,
                                  true=if_true[0], false=if_false[0] if if_false else None)
            if_branch.true.from_node = if_branch
            # Make sure that the false branch knows it's predecessor is the if-statement.
            # This is ensure due to single-line if-statements not having a false branch in the AST.
            if if_branch.false:
                if_branch.false.from_node = if_branch
            return if_branch
        if (isinstance(statement, c_ast.While)):
            if_true = list(map(lambda s: parse_node(s, next=next),
                               statement.stmt)) if statement.stmt else []
            link(if_true)
            while_branch = CFGBranch(
                type=type_while, current_node=statement, true=if_true[0], false=next)
            if_true[-1].to_node = while_branch
            while_branch.true.from_node = while_branch
            return while_branch
        if (isinstance(statement, c_ast.FuncCall)):
            if (hasattr(statement.name, "name") and statement.name.name == "output"):
                argument = parse_node(statement.args.exprs[0])
                return CFGNode(type=type_output, current_node=statement, lvalue=argument)
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


def print_cfg(node):
    def cfg_to_str(node, acc="", indent=0, extra_info=""):
        indentation = "\t" * indent
        to_add = f"\n{indentation}⭣ {extra_info}\n{indentation}{node.type}"
        if (node.to_node):
            true = ""
            false = ""
            if (node.to_node.type == type_while):
                return acc + to_add  # Stops infinite recursion.
            if isinstance(node, CFGBranch):
                true = cfg_to_str(node.true, indent=indent +
                                  1, extra_info="true")
                false = cfg_to_str(
                    node.false, indent=indent+1, extra_info="false")
                to_add += f"{true+false}"
                return cfg_to_str(node.to_node, indent=indent+1, acc=acc + to_add)
            return cfg_to_str(node.to_node, acc + to_add)
        else:
            return acc + to_add

    to_print = cfg_to_str(node)
    print(to_print)

# Terrible inefficient cfg to list


def cfg_to_list(cfg):
    q = queue.SimpleQueue()
    q.put(cfg)
    cfgl = []
    while not q.empty():
        top = q.get()
        if top == None:
            continue
        # this is soo bad...
        cfgl.append(top)
        if top.is_condition():
            if not (top.true in cfgl):
                q.put(top.true)
            if not (top.false in cfgl):
                q.put(top.false)
        else:
            if not (top.to_node in cfgl):
                q.put(top.to_node)
    return cfgl


def get_expressions_in_program(cfg_list) -> frozenset:
    expressions = []
    for x in cfg_list:
        if x.rval != None:
            expressions.append(x.rval)
    return frozenset(expressions)


def get_variables_in_program(cfg_list) -> frozenset:
    # We only consider declared variables and global scope
    l = []
    for x in cfg_list:
        if x.is_declaration():
            l.append(x.lval)
    return frozenset(l)

# super inefficient back pointers fixer
# It also sets the pred list in CFGANode


def from_node_fixer(cfg_list):
    # Fix from_node pointers, but it is super expensive
    # on the other hand the graphs are quite small
    for x in cfg_list:
        back_ptrs = []
        for y in cfg_list:
            if y.is_condition():
                if y.true == x or y.false == x:
                    back_ptrs.append(y)
            else:
                if y.to_node == x:
                    back_ptrs.append(y)

        if back_ptrs != []:
            x.from_node = back_ptrs
        else:
            x.from_node = None  # Just to keep the original convention
        x.pred = back_ptrs

# to_node and true/false pointers to successors list


def to_node_to_succ(cfg_list):
    for x in cfg_list:
        if x.is_condition():
            x.succ = [x.true, x.false]
        else:
            x.succ = [x.to_node]


# Adds entry and exit nodes to the cfg
def add_entry_exit_nodes(cfg_list) -> CFGNode:
    entry_point = []
    exit_points = []

    for x in cfg_list:
        if x.from_node == None:
            entry_point.append(x)
        if x.to_node == None:
            exit_points.append(x)
    # sanity check
    assert(len(entry_point) == 1)
    entry = CFGNode(type=type_entry, to_node=entry_point[0])
    exit_node = CFGNode(type=type_exit, from_node=exit_points)
    for x in exit_points:
        x.to_node = exit_node
    return entry
