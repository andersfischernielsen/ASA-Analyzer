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
    
    def max_upper_bound(self, left:frozenset, right:frozenset): 
        return left.intersection(right)

    def calculate_lattice_element(self, node): 
        # TODO: Implement
        return None

class CFGNode(): 
    def __init__(self, type, from_node, to_node, lvalue=None, rvalue=None):
        self.type = type
        self.from_node = from_node
        self.to_node = to_node
        self.lvalue = lvalue
        self.rvalue = rvalue
    
    def __str__(self):
        return f"[{self.type}: (lvalue: {self.lvalue}, rvalue: {self.rvalue})]"

class CFGBranch(): 
    def __init__(self, type, from_node, left, right):
        self.type = type
        self.from_node = from_node
        self.left = left
        self.right = right

    def __str__(self):
        left_strings = map(lambda n: str(n), self.left)
        right_strings = map(lambda n: str(n), self.right)
        left_joined = str.join(", ", left_strings)
        right_joined = str.join(", ", right_strings)
        return f"[{self.type}: left: {left_joined}, right: {right_joined}]"

type_assignment = "Assignment"
type_if = "If"
type_declaration = "Declaration"
type_while = "While"
type_binary_operator = "BinaryOperator"
type_return = "Return"
type_constant = "Constant"
type_variable = "Variable"