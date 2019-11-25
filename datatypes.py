from typing import Callable

environment = []

class Analysis:
    transfer_functions: [Callable[[list, str, str], list]]

    def __init__(self, transfer_functions):
        self.transfer_functions = transfer_functions

    def get_transfer_functions(self):
        return self.transfer_functions

class CFGNode(): 
    def __init__(self, type, from_node, to_node, lvalue=None, rvalue=None):
        self.type = type
        self.from_node = from_node
        self.to_node = to_node
        self.lvalue = lvalue
        self.rvalue = rvalue
    
    def __str__(self):
        return f"[{self.from_node} -> {self.to_node}]"
    
    def __repr__(self):
        return f"[{self.from_node} -> {self.to_node}]"

class CFGBranch(): 
    def __init__(self, type, from_node, left, right):
        self.type = type
        self.from_node = from_node
        self.left = left
        self.right = right

    def __str__(self):
        return f"[{self.from_node} -left-> {self.left} -right-> {self.right}]"

    def __repr__(self):
        return f"[{self.from_node} -left-> {self.left} -right-> {self.right}]"

type_assignment = "Assignment"
type_if = "If"
type_declaration = "Declaration"
type_while = "While"
type_binary_operator = "BinaryOperator"
type_return = "Return"