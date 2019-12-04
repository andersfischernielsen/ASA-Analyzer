from datatypes import *

def exit(ana, node):
    return frozenset()

def cond_out(ana, node: CFGNode):
    return least_upper_bound(join_least_upper_bound(ana, node), node.r_variables)

def assign(ana, node):
    join_variables = (join_least_upper_bound(ana, node)).difference(node.l_var)
    return ana.lub(join_variables, node.r_variables)

def decl(ana, node):
    return (join_least_upper_bound(ana, node)).difference(cfg.variable_set)

def rest(ana, node):
    return join_least_upper_bound(ana, node)

transfer_functions = {
    type_exit: [exit],
    type_assignment: [assign],
    type_declaration: [decl],
    type_all: [rest]
}

analysis = Analysis(transfer_functions=transfer_functions)