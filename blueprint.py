

#A CFGNode
class CFGNode:
    #Creates a new CFGNode
    #ident a numerical ident for the node
    #lvar is the left hand side (if any)
    #rvars the set of variables happening on the right hand side
    #succs the successors list
    #preds the predecessors list
    #typeof the type of node: assignment, boolean exp, etc.
    def __init__(self, ident, lvar, rexp,succs,preds,typeof):
        self.ident = ident
        self.lvar = lvar
        rv = self.__exp_vars(rexp)
        if rv == []:
            self.rvars = frozenset()
        else:
            self.rvars = frozenset(rv)
        self.rexprs = frozenset()
        self.rstr = self.__expr_to_str(rexp) #right hand side str rep + expressions calculation
        self.succs = succs
        self.preds = preds
        self.typeof = typeof

    def __str__(self):
        if self.is_output():
            return "output " + self.rstr
        if self.is_assignment():
            var = ''
            #self.lvar should be of cardinality 1
            for x in self.lvar:
                var = x
            return var + " = " + self.rstr
        if self.is_declaration():
            var = ''
            #self.lvar should be of cardinality 1
            for x in self.lvar:
                var = x
            return "var "+var
        if self.is_condition():
            return "cond " + self.rstr
        if self.is_entry():
            return "entry"
        if self.is_exit():
            return "exit"
        return "to do"
    #Extractor of variables in an expression in polish form
    def __exp_vars(self,exp):
        if exp == []:
            return []
        if len(exp) == 1:
            if exp[0].isnumeric():
                return []
            return exp
        evars = []
        if type(exp[1]) == str and not (exp[1]).isnumeric():
            evars += [exp[1]]
        else:
            evars += self.__exp_vars(exp[1])
        if type(exp[2]) == str and not (exp[2]).isnumeric():
            evars += [exp[2]]
        else:
            evars += self.__exp_vars(exp[2])
        return evars
    #Exprs set from polish form
    def __expr_to_str(self,exp):
        if type(exp) == str:
            return exp
        if exp == []:
            return ''
        if len(exp) == 1:
            return exp[0]
        s = self.__expr_to_str(exp[1]) + exp[0] + self.__expr_to_str(exp[2])
        self.rexprs = self.rexprs.union(frozenset([s]))
        return s
    
    def _is_something(self, something):
        return self.typeof == something
    def is_assignment(self):
        return self._is_something('assignment')
    def is_declaration(self):
        return self._is_something('decl')
    def is_condition(self):
        return self._is_something('cond')
    def is_output(self):
        return self._is_something('output')
    def is_exit(self):
        return self._is_something('exit')
    def is_entry(self):
        return self._is_something('entry')
#A CFG
class CFG:
    def __init__(self, cfgn_list):
        self.cfg = cfgn_list
        self.__vset_eset()

    def __vset_eset(self):
        vset = []
        self.exprs_set = frozenset()
        for x in self.cfg:
            if x.is_declaration():
                vset += x.lvar
            self.exprs_set = self.exprs_set.union(x.rexprs)
        self.vars_set = frozenset(vset)
    def size(self):
        return len(self.cfg)

    def __iter__(self):
        return self.cfg.__iter__()


# Analysis class for lattice-based analysis
class Analysis:
    
    #Creates an Analyis for the given:
    #cfg - A CFG
    #vset - The set of variables that happen in cfg
    #eset - The set of expressions that happen in cfg
    #mfun - Monotone functions
    def __init__(self, cfg, mon_funs):
        self._state = [frozenset()]*cfg.size()
        self.mon_funs = mon_funs
        self.cfg = cfg
    #Private wrapper for the user supplied
    #analysis functions
    def _f_wrapper(self, cfgnode):
        for x in self.mon_funs:
            res = x(self,cfgnode)
            if res != None:
                return res
        return None #Should not happen
        
    #Returns the least upper bound
    #between left and right lattice (set) elements
    def lub(self, left, right):
        tl = type(left)
        tr = type(right)
        if tl == tr and tl is frozenset:
            return left.union(right)
         

    #Returns the maximal lower bound
    #between left and right lattice (set) elements
    def glb(self, left, right):
        tl = type(left)
        tr = type(right)
        if tl == tr and tl is frozenset:
            return left.intersection(right)

    def state(self, cfgnode):
        if type(cfgnode) == int:
            return self._state[cfgnode]
        elif type(cfgnode) == CFGNode:
            return self._state[cfgnode.ident]
        return None

    def fix_point(self):
        reached = False
        while not reached:
            reached = True
            for x in self.cfg:
                res_x = self._f_wrapper(x)
                if res_x != self._state[x.ident]:
                    reached = False
                    self._state[x.ident] = res_x

    def __str__(self):
        r = ''
        for (i,x) in enumerate(self._state):
            s = x.__str__()
            if s == 'frozenset()':
                s = '{}'
            else:
                s = x.__str__().replace('frozenset(','').replace(')','')
            r += self.cfg.cfg[i].__str__() + "\t--->\t"+ s + '\n'
        return r            
################################### EXAMPLES ###############################################
                    
########## Example program ##########
#Liveness & Reaching definitions
#var x;
#var y;
#var z;
#x = input;
#while( x > 1) {
#   y = x/2;
#   if( y > 3)
#      x = x - y;
#   z = x - 4;
#   if (z > 0)
#       x = x/2;
#   z = z-1;
#}
#output x
########## Example program ##########

nodes = []
nodes.append(CFGNode(0, frozenset(['x']), [],[1],[],'decl'))
nodes.append(CFGNode(1, frozenset(['y']), [],[2],[0],'decl'))
nodes.append(CFGNode(2, frozenset(['z']), [],[3],[1],'decl'))
nodes.append(CFGNode(3, frozenset(['x']), [],[4],[2],'assignment'))
nodes.append(CFGNode(4, frozenset(), ['>','x','1'],[5,12],[11],'cond'))
nodes.append(CFGNode(5, frozenset(['y']),['/','x','2'],[6],[4],'assignment'))
nodes.append(CFGNode(6, frozenset(), ['>','y','3'],[7,8],[5],'cond'))
nodes.append(CFGNode(7, frozenset(['x']), ['-','x','y'],[6],[8],'assignment'))
nodes.append(CFGNode(8, frozenset(['z']), ['-','x','4'],[9],[6,7],'assignment'))
nodes.append(CFGNode(9, frozenset(), ['>','z','0'],[10,11],[8],'cond'))
nodes.append(CFGNode(10, frozenset(['x']),['/','x','2'],[9],[11],'assignment'))
nodes.append(CFGNode(11, frozenset(['z']), ['-','z','1'],[4],[9,10],'assignment'))
nodes.append(CFGNode(12, frozenset(),['x'],[13],[4],'output'))
nodes.append(CFGNode(13, frozenset(),[],[],[12],'exit'))
cfg = CFG(nodes)

########## Example program ##########
#Available expressions
#var x;
#var y;
#var z;
#var a;
#var b;
#z = a+b;
#y = a*b;
#while( y > a+b) {
#   a = a+1;
#   x = a+b;
#}
########## Example program ##########
nodes1 = []
nodes1.append(CFGNode(0,frozenset(),[],[1],[],'entry'))
nodes1.append(CFGNode(1,frozenset(['x']),[],[2],[0],'decl'))
nodes1.append(CFGNode(2,frozenset(['y']),[],[3],[1],'decl'))
nodes1.append(CFGNode(3,frozenset(['z']),[],[4],[2],'decl'))
nodes1.append(CFGNode(4,frozenset(['a']),[],[5],[3],'decl'))
nodes1.append(CFGNode(5,frozenset(['b']),[],[6],[4],'decl'))
nodes1.append(CFGNode(6,frozenset(['z']),['+','a','b'],[7],[5],'assignment'))
nodes1.append(CFGNode(7,frozenset(['y']),['*','a','b'],[8],[6],'assignment'))
nodes1.append(CFGNode(8,frozenset(),['>','y',['+','a','b']],[9,11],[7],'cond'))
nodes1.append(CFGNode(9,frozenset(['a']),['+','a','1'],[10],[8],'assignment'))
nodes1.append(CFGNode(10,frozenset(['x']),['*','a','b'],[8],[9],'assignment'))
nodes1.append(CFGNode(11,frozenset(),[],[],[8],'exit'))

cfg1 = CFG(nodes1)

########## Example program ##########
#Very busy expressions
#var x;
#var a;
#var b;
#x = input
#a = x-1;
#b = x-2;
#while( x > 0) {
#   output a*b-x;
#   x = x-1;
#}
#output a*b
########## Example program ##########
nodes2 = []
nodes2.append(CFGNode(0,frozenset(),[],[1],[],'entry'))
nodes2.append(CFGNode(1,frozenset(['x']),[],[2],[0],'decl'))
nodes2.append(CFGNode(2,frozenset(['a']),[],[3],[1],'decl'))
nodes2.append(CFGNode(3,frozenset(['b']),[],[4],[2],'decl'))
nodes2.append(CFGNode(4,frozenset(['a']),['-','x','1'],[5],[3],'assignment'))
nodes2.append(CFGNode(5,frozenset(['b']),['-','x','2'],[6],[4],'assignment'))
nodes2.append(CFGNode(6,frozenset(),['>','x','0'],[7,9],[5],'cond'))
nodes2.append(CFGNode(7,frozenset(),['-',['*','a','b'],'x'],[8],[6],'output'))
nodes2.append(CFGNode(8,frozenset(['x']),['-','x','1'],[6],[7],'assignment'))
nodes2.append(CFGNode(9,frozenset(),['*','a','b'],[10],[6],'output'))
nodes2.append(CFGNode(10,frozenset(),[],[],[9],'exit'))

cfg2 = CFG(nodes2)



####################### Liveness ##############################

def join_lub(ana,cfgn):
    club = frozenset()
    for n in cfgn.succs:
        club = ana.lub(club,ana.state(n))
    return club

#The user only defines one single function for the fix-point calculation
def only_one_liveness(ana,cfgn):
    jvars = join_lub(ana,cfgn)
    if cfgn.is_output() or cfgn.is_condition():
        return ana.lub(jvars,cfgn.rvars)
    if cfgn.is_assignment():
        return ana.lub(jvars.difference(cfgn.lvar),cfgn.rvars)
    if cfgn.is_declaration():
        return jvars.difference(cfg.vars_set)
    return jvars
        


#The user defines a set of functions for the fix-point calculation
#The wrapper executes each function in order and returns the first
#None value 
def exit(ana,cfgn):
    if cfgn.is_exit():
        return frozenset()
    return None

def cond_out(ana,cfgn):
    if not (cfgn.is_output() or cfgn.is_condition()):
        return None
    return ana.lub(join_lub(ana,cfgn),cfgn.rvars)

def assign(ana,cfgn):
    if not cfgn.is_assignment():
        return None
    jvars = (join_lub(ana,cfgn)).difference(cfgn.lvar)
    return ana.lub(jvars,cfgn.rvars)

def decl(ana,cfgn):
    if not cfgn.is_declaration():
        return None
    return (join_lub(ana,cfgn)).difference(cfg.vars_set)

def rest(ana,cfgn):
    return join_lub(ana,cfgn)

#Fix-point with just one function
ana = Analysis(cfg,[only_one_liveness])
ana.fix_point()
print('Just one function to perform the analysis\n')
print(ana)

#Fix-point with several functions
ana = Analysis(cfg, [cond_out,assign,decl,rest])
ana.fix_point()
print('\nSeveral functions that together do the analysis\n')
print(ana)

####################### End: Liveness ##############################


####################### Available expressions ##############################
def join_glb(ana,cfgn):
    if len(cfgn.preds) == 0:
        return frozenset()
    cglb = ana.state(cfgn.preds[0])
    for n in cfgn.preds:
        cglb = ana.glb(cglb,ana.state(n))
    return cglb

def only_one_avail_exprs(ana,cfgn):
    if cfgn.is_entry():
        return frozenset()
    jexps = join_glb(ana,cfgn)
    if cfgn.is_condition() or cfgn.is_output():
        return ana.lub(jexps,cfgn.rexprs)
    
    if cfgn.is_assignment():
        fset = frozenset()
        tset = ana.lub(jexps,cfgn.rexprs)
        var = ''
        #cfgn.lvar should be of cardinality 1
        for x in cfgn.lvar:
            var = x
            
        for x in tset:
            if not (var in x):
                fset = fset.union(frozenset([x]))
        return fset
    return jexps

ana1 = Analysis(cfg1,[only_one_avail_exprs])
ana1.fix_point()
print('\n\nAvailable expressions example:\n')
print(ana1)
####################### End: Available expressions ##############################

####################### Very Busy Expressions ##############################
def join_glb_succs(ana,cfgn):
    if len(cfgn.succs) == 0:
        return frozenset()
    cglb = ana.state(cfgn.succs[0])
    for n in cfgn.succs:
        cglb = ana.glb(cglb,ana.state(n))
    return cglb

def only_one_busy_exprs(ana,cfgn):
    if cfgn.is_exit():
        return frozenset()
    jexps = join_glb_succs(ana,cfgn)
    if cfgn.is_condition() or cfgn.is_output():
        return ana.lub(jexps,cfgn.rexprs)
    if cfgn.is_assignment():
        fset = frozenset()
        var = ''
        #cfgn.lvar should be of cardinality 1
        for x in cfgn.lvar:
            var = x
        for x in jexps:
            if not (var in x):
                fset = fset.union(frozenset([x]))
        return ana.lub(fset,cfgn.rexprs)
    return jexps

ana2 = Analysis(cfg2,[only_one_busy_exprs])
ana2.fix_point()
print('\n\nVery Busy Expressions example:\n')
print(ana2)

####################### End: Very Busy Expressions ##############################
    
