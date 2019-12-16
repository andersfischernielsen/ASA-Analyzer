#Liveness analysis example

from datatypes import type_assignment, type_declaration, type_if, type_while,type_entry,type_exit,type_output,\
    type_input

def join_glb(analysis,cfgn):
    if len(cfgn.pred) == 0:
        return frozenset()
    cglb = analysis.state[cfgn.pred[0]]
    for n in cfgn.pred:
        cglb = analysis.greatest_lower_bound(cglb,analysis.state[n])
    return cglb

def entry(analysis,cfgn):
    return frozenset()

def condition_output(analysis, cfgn):
    return analysis.least_upper_bound(join_glb(analysis,cfgn),cfgn.rval.sub_exprs())

def assign(analysis,cfgn):
    jexprs = join_glb(analysis,cfgn)
    tset = analysis.least_upper_bound(jexprs,cfgn.rval.sub_exprs())
    fset = frozenset()
    for x in tset:
        if not x.var_in(cfgn.lval):
            fset = fset.union(frozenset([x]))
    return fset




m_funs = {
    type_assignment:assign,
    type_declaration:join_glb,
    type_if:condition_output,
    type_while:condition_output,
    type_entry:entry,
    type_exit:join_glb,
    type_output:condition_output,
    type_input:join_glb
    
}
from datatypes import Analysis
analysis = Analysis(monotone_functions=m_funs)


