from typing import Callable

# Analysis class for lattice-based analysis
class Analysis:
    #Creates an Analyis for the given:
    #cfg - A CFG
    #vset - The set of variables that happen in cfg
    #eset - The set of expressions that happen in cfg
    #mfun - Monotone functions
    def __init__(self, monotone_functions):
        self.monotone_functions = monotone_functions

class CFG:
    def __init__(self, node_list: [CFGNode]):
        self.cfg = node_list
        self.__variable_set_expression_set()

    def __variable_set_expression_set(self):
        variable_set = []
        self.expression_set = frozenset()
        for node in self.cfg:
            if node.type is type_declaration:
                variable_set += node.l_var
            self.expression_set = self.expression_set.union(node.r_expressions)
        self.variable_set = frozenset(variable_set)
    
    def size(self):
        return len(self.cfg)

    def __iter__(self):
        return self.cfg.__iter__()
    
#Returns the least upper bound between left and right lattice elements
def least_upper_bound(self, left, right):
    tl = type(left)
    tr = type(right)
    if tl == tr and tl is frozenset:
        return left.union(right)
        
#Returns the maximal lower bound between left and right lattice elements
def maximal_lower_bound(self, left, right):
    type_left = type(left)
    type_right = type(right)
    if type_left == type_right and type_left is frozenset:
        return left.intersection(right)

def join_least_upper_bound(state, node):
    result = frozenset()
    for n in node.succs:
        result = least_upper_bound(result, state)
    return result

class CFGNode(): 
    #Creates a new CFGNode
    #identifier a numerical identifier for the node
    #l_var is the left hand side (if any)
    #r_vars the set of variables happening on the right hand side
    #successors the successors list
    #predecessors the predecessors list
    #type: assignment, boolean exp, etc.
    def __init__(self, identifier, l_var, r_exp, successors, predecessors, type):
        self.identifier = identifier
        self.l_var = l_var
        r_variables = self.__get_expression_variables(r_exp)
        self.r_variables = frozenset(r_variables)
        self.__expr_to_str(r_exp)
        self.successors = successors
        self.predecessors = predecessors
        self.type = type
    
    def __str__(self):
        return f"[{self.type}: (lvalue: {self.lvalue}, rvalue: {self.rvalue})]"

    #Extractor of variables in an expression in polish form
    def __get_expression_variables(self, expression):
        if expression == []:
            return []
        
        if len(expression) == 1:
            if expression[0].isnumeric():
                return []
            return expression
        
        expression_variables = []

        if type(expression[1]) == str and not (expression[1]).isnumeric():
            expression_variables += [expression[1]]
        else:
            expression_variables += self.__get_expression_variables(expression[1])
        
        if type(expression[2]) == str and not (expression[2]).isnumeric():
            expression_variables += [expression[2]]
        else:
            expression_variables += self.__get_expression_variables(expression[2])

        return expression_variables
    
    #Exprs set from polish form
    def __expression_to_string(self, expression):
        if type(expression) == str:
            return expression

        if expression == []:
            return ''

        if len(expression) == 1:
            return expression[0]

        s = self.__expression_to_string(expression[1]) + expression[0] + self.__expression_to_string(expression[2])
        return s

type_assignment = "Assignment"
type_if = "If"
type_declaration = "Declaration"
type_while = "While"
type_return = "Return"
type_constant = "Constant"
type_variable = "Variable"
type_output = "Output"
type_condition = "Condition"
type_exit = "Exit"
type_entry = "Entry"
type_all = "All"