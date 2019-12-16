from typing import Callable
import pycparser

class Analysis:
    monotone_functions: [Callable[[list, str, str], list]]
    variables: frozenset
    expressions: frozenset

    def __init__(self, monotone_functions, variables=None, expressions=None):
        self.monotone_functions = monotone_functions
        self.variables = variables
        self.expressions = expressions

    #Initialize the state of each block
    def init_state(self, cfg_list):
        self.cfg_list = cfg_list
        self.state = {}
        for x in self.cfg_list:
            self.state[x] = frozenset()

    def get_monotone_functions(self):
        return self.monotone_functions

    def least_upper_bound(self, left:frozenset, right:frozenset):
        return left.union(right)
    
    def maximal_lower_bound(self, left:frozenset, right:frozenset): 
        return left.intersection(right)

    #Returns the 'state' of the analysis for the given cfg node
    def state(self, cfgn):
        return self.state[cfgn]

    def calculate_lattice_element(self, node): 
        # TODO: Implement
        return None

#Expr wrapper for pycparser expressions.
#This wrapper is hashable and equality capable
class Expr():
    def __init__(self,expr):
        self.op = None
        self.l = None
        self.r = None
        self.str_rep = None
        self.vars_in = frozenset()
        if type(expr) == pycparser.c_ast.ID:
            self.l = expr.name
            self.str_rep = self.l
        if type(expr) == pycparser.c_ast.Constant:
            self.l = expr.value
            self.str_rep = self.l
        if type(expr) == pycparser.c_ast.BinaryOp:
            self.op = expr.op
            self.l = Expr(expr.left)
            self.r = Expr(expr.right)
            self.str_rep = str(self.l)+self.op+str(self.r)
        self.vars_in = frozenset(Expr.__exp_vars(expr))
    def __str__(self):
        return self.str_rep

    def __eq__(self, exp):
        if type(exp) != type(self):
            return False
        return self.str_rep == exp.str_rep

    def __hash__(self):
        return self.str_rep.__hash__()

    #Extracts the variables happening in the Exprs
    def __exp_vars(expr):
        if type(expr) == pycparser.c_ast.BinaryOp:
            return Expr.__exp_vars(expr.left) + Expr.__exp_vars(expr.right)
        if type(expr) == pycparser.c_ast.ID:
            return [expr.name]
        return []
    

    #Checks if var happens in the expression
    def var_in(self, var):
        if self.op != None:
            return self.l.var_in(var) or self.r.var_in(var)
        return self.l == var


class CFGANode():
    def __init__(self,t,ast_val=None):
        self.type = t
        self.lval = None
        self.rval = None
        self.pred = []
        self.succ = []
        if ast_val != None:
            if type(ast_val) == pycparser.c_ast.Decl:
                self.lval = ast_val.name
            if type(ast_val) == pycparser.c_ast.Assignment:
                self.lval = ast_val.lvalue.name
                self.rval = Expr(ast_val.rvalue)
            if type(ast_val) == pycparser.c_ast.If or \
               type(ast_val) == pycparser.c_ast.While:
                self.rval = Expr(ast_val.cond)
        if self.type == type_output:
            self.rval = Expr(ast_val.args.exprs[0])
        

    #Is type functions...
    #generic checker
    def _is_node_type(self, qtype):
        return self.type == qtype
    def is_assignment(self):
        return self._is_node_type(type_assignment)
    def is_declaration(self):
        return self._is_node_type(type_declaration)
    def is_constant(self):
        return self._is_node_type(type_constant)
    def is_condition(self):
        return self._is_node_type(type_if) or self._is_node_type(type_while)
    def is_return(self):
        return self._is_node_type(type_return)
    def is_input(self):
        return self._is_node_type(type_input)

class CFGNode(CFGANode): 
    def __init__(self, type, from_node=None, current_node=None, to_node=None, lvalue=None, rvalue=None):
        CFGANode.__init__(self,type,current_node)
        self.from_node = from_node
        self.to_node = to_node
        self.current_node = current_node
        self.lvalue = lvalue
        self.rvalue = rvalue
    
    def __str__(self):
        return f"[{self.type}: (lvalue: {self.lvalue}, rvalue: {self.rvalue})]"

class CFGBranch(CFGANode): 
    def __init__(self, type, from_node=None, to_node=None, current_node=None, true=None, false=None):
        self.from_node = from_node
        self.current_node = current_node
        self.true = true
        self.false = false
        CFGANode.__init__(self,type,current_node)

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
type_entry = "Entry"
type_exit = "Exit"
type_output = "Output"
type_input = "Input"
