import datatypes

def set_name_zero (node):
    if (node.rvalue == "0"):
        return (node.lvalue, "0")

def set_name_not_zero (node):
    if (node.rvalue != "0"):
        return (node.lvalue,"!0")

def decl (node):
    return (node.lvalue,"bottom")

transfer_functions = {
    "Assignment": [set_name_zero, set_name_not_zero],
    "Declaration": [decl]
}

from datatypes import Analysis

analysis = Analysis(transfer_functions=transfer_functions)