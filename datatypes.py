from typing import Callable

environment = []

class Analysis:
    transfer_functions: [Callable[[list, str, str], list]]

    def __init__(self, transfer_functions):
        self.transfer_functions = transfer_functions

    def get_transfer_functions(self):
        return self.transfer_functions

class CFGNode(): 
    def __init__(self, from_node, to_node):
        self.from_node = from_node
        self.to_node = to_node
    
    def __str__(self):
        return f"[{self.from_node} -> {self.to_node}]"
    
    def __repr__(self):
        return f"[{self.from_node} -> {self.to_node}]"

class CFGBranch(): 
    def __init__(self, from_node, left, right):
        self.from_node = from_node
        self.left = left
        self.right = right

    def __str__(self):
        return f"[{self.from_node} -left-> {self.left} -right-> {self.right}]"

    def __repr__(self):
        return f"[{self.from_node} -left-> {self.left} -right-> {self.right}]"

available_cfg_types = ["Assignment", "If", "Decl", "While"]