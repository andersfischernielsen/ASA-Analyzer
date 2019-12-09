from typing import Callable

class Analysis:
    transfer_functions: [Callable[[list, str, str], list]]
    variables: frozenset
    expressions: frozenset

    def __init__(self, transfer_functions, variables=None, expressions=None):
        self.transfer_functions = transfer_functions
        self.variables = variables
        self.expressions = expressions

    def get_transfer_functions(self):
        return self.transfer_functions

    def least_upper_bound(self, left:frozenset, right:frozenset):
        return left.union(right)
    
    def maximal_lower_bound(self, left:frozenset, right:frozenset): 
        return left.intersection(right)

    def calculate_lattice_element(self, node): 
        # TODO: Implement
        return None

class CFGNode(): 
    def __init__(self, type, from_node=None, current_node=None, to_node=None, lvalue=None, rvalue=None):
        self.type = type
        self.from_node = from_node
        self.to_node = to_node
        self.current_node = current_node
        self.lvalue = lvalue
        self.rvalue = rvalue
    
    def __str__(self):
        return f"[{self.type}: (lvalue: {self.lvalue}, rvalue: {self.rvalue})]"

class CFGBranch(): 
    def __init__(self, type, from_node=None, to_node=None, current_node=None, true=None, false=None):
        self.type = type
        self.from_node = from_node
        self.current_node = current_node
        self.true = true
        self.false = false

    def __str__(self):
        to_print = "While" if self.to_node.type == "While" else self.to_node
        return f"[{self.type}: true: {self.true}, false: {self.false}]"

type_assignment = "Assignment"
type_declaration = "Declaration"
type_constant = "Constant"
type_variable = "Variable"
type_binary_operator = "BinaryOperator"
type_if = "If"
type_while = "While"
type_return = "Return"