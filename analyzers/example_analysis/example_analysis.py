import datatypes

def set_name_zero (node):
    if (node.rvalue.value == "0"):
        return (node.lvalue.name, "0")

def set_name_not_zero (node):
    if (node.rvalue.value != "0"):
        return (node.lvalue.name,"!0")

def decl (node):
    return (node.name,"bottom")

transfer_functions = {
    "Assignment": set_name_zero,
    "Assignment": set_name_not_zero,
    "Decl": decl
}

from datatypes import Lattice, Analysis

analysis = Analysis(transfer_functions=transfer_functions)