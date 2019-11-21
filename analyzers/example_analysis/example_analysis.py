import pycparser

def set_decl_bottom (env, node):
    if isinstance(node, pycparser.c_ast.Decl):
        env[node.name] = "bottom"
    
    return env

def set_decl_top (env, node):
    if isinstance(node, pycparser.c_ast.Decl):
        env[node.name] = "top"
    
    return env

def set_name_zero (env, node):
    if isinstance(node, pycparser.c_ast.Assignment):
        if (node.rvalue.value == "0"):
            env[node.lvalue.name] = "0"
    
    return env

def set_name_not_zero (env, node):
    if isinstance(node, pycparser.c_ast.Assignment):
        if (node.rvalue.value != "0"):
            env[node.lvalue.name] = "!0"
    
    return env

transfer_functions = [
    (lambda env, _: env),
    set_decl_bottom,
    set_decl_top,
    set_name_zero,
    set_name_not_zero
]

def order(a, b):
    if (a == "bottom" and b == "top"): return -1
    if (a == "bottom" and b == "0"): return -1
    if (a == "bottom" and b == "!0"): return -1
    if (a == "bottom" and b == "bottom"): return 0
    if (a == "top" and b == "bottom"): return 1
    if (a == "top" and b == "0"): return 1
    if (a == "top" and b == "!0"): return 1
    if (a == "top" and b == "top"): return 0
    if (a == "0" and b == "!0"): return 0
    if (a == "0" and b == "top"): return -1
    if (a == "0" and b == "bottom"): return 1
    if (a == "0" and b == "0"): return 0
    if (a == "!0" and b == "0"): return 0
    if (a == "!0" and b == "top"): return -1
    if (a == "!0" and b == "bottom"): return 1
    if (a == "!0" and b == "!0"): return 0
    
    else: 
        raise NameError()

from datatypes import Lattice, Analysis

lattice = Lattice(symbols=[
        ("bottom", "unknown"),
        ("top", "is either zero or not zero"),
        ("0", "must be zero"),
        ("!0", "may be not zero")
    ],
    ordering=order)

analysis = Analysis(lattice=lattice, transfer_functions=transfer_functions)