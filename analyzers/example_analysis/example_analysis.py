from datatypes import type_assignment, type_declaration, type_binary_operator

def set_name_zero (node):
    if (isinstance(node.rvalue.lvalue, str)):
        if (node.rvalue.lvalue != "0"):
            return "0"
    if (node.rvalue.lvalue == "0"):
        return "top"

def set_name_not_zero (node):
    if (isinstance(node.rvalue.lvalue, str)):
        if (node.rvalue.lvalue != "0"):
            return "!0"
    else:     
        return "top"

def binary_operator(node):
    if (node.rvalue.lvalue == "0") and (node.lvalue.lvalue == "0"):
        return "0"
    if (node.rvalue.lvalue == "!0") and (node.lvalue.lvalue == "0"):
        return "top"
    if (node.rvalue.lvalue == "!0") and (node.lvalue.lvalue == "!0"):
        return "!0"
    if (node.rvalue.lvalue == "0") and (node.lvalue.lvalue == "!0"):
        return "top"

def decl (node):
    return "bottom"

monotone_functions = {
    type_assignment: [set_name_zero, set_name_not_zero],
    type_declaration: [decl],
    type_binary_operator: [binary_operator]
}

from datatypes import Analysis

analysis = Analysis(monotone_functions=monotone_functions)