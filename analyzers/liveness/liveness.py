#Liveness analysis example

def join_lub(analysis,cfgn):
    club = frozenset()
    for n in cfgn.succ:
        club = analysis.least_upper_bound(club,analysis.state())
    return club

def exitn(analysis,cfgn):
    return frozenset()

def condition_output(analysis, cfgn):
    return analysis.lub(join_lub(analysis,cfgn),cfgn.rval.vars_in)

def assign(analysis,cfgn):
    jvars = (join_lub(analysis,cfgn)).difference(cfgn.lvar)
    return analysis.least_upper_bound(jvars,cfgn.rval.vars_in)

def decl(analysis,cfgn):
    join_lub(analysis,cfgn).difference(analysis.variables)




m_funs = {
    type_assignment:[assign],
    type_declaration:[decl],
    type_if:[condition_output],
    type_while:[condition_output],
    type_entry:[join_lub],
    type_exit:[exitn],
    type_output:[condition_output]
    
}
from datatypes import Analysis
analysis = Analysis(monotone_functions=m_funs)


