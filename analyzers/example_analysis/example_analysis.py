import pycparser

def set_name_zero (node):
    if isinstance(node, pycparser.c_ast.Assignment):
        if (node.rvalue.value == "0"):
            return (node.lvalue.name, "0")

def set_name_not_zero (node):
    if isinstance(node, pycparser.c_ast.Assignment):
        if (node.rvalue.value != "0"):
            return (node.lvalue.name,"!0")

def decl (node):
    if isinstance(node, pycparser.c_ast.Decl):
        return (node.name,"bottom")

transfer_functions = [
    set_name_zero,
    set_name_not_zero,
    decl
]

from datatypes import Lattice, Analysis

lattice = Lattice(symbols={
        "bottom": "unknown",
        "top": "is either zero or not zero",
        "0": "must be zero",
        "!0": "may be not zero"
    })

analysis = Analysis(lattice=lattice, transfer_functions=transfer_functions)