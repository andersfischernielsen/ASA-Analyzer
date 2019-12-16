from datatypes import CFGNode, CFGBranch



def find_fixpoint(analysis):
    reached = False #is fix point found?
    while not reached:
        reached = True
        for x in analysis.cfg_list:
            mon_fun= analysis.monotone_functions[x.type]
            cres = mon_fun(analysis,x)
            if cres != analysis.state[x]:
                reached = False
                analysis.state[x] = cres

    for x in analysis.state:
        print(x)
        print(analysis.state[x])
        print('------')


#def find_fixpoint(cfg, transfer_functions) -> {}:
#    def apply_transfer_functions(cfg, transfer_functions) -> {}:
#        def apply(node):
#            if (isinstance(node, CFGNode)):
#                matching_functions = transfer_functions.get(node.type)
#                if (matching_functions is None):
#                    return ["bottom"]
#
#                for t in matching_functions:
#                    res = t(node)
#                    if res is not None: 
#                        return [res]
#
#            elif (isinstance(node, CFGBranch)):
#                left = []
#                for l in (node.left):
#                    left.append(apply(l))
#                right = []
#                for l in (node.right):
#                    right.append(apply(l))
#                # TODO: Conjunction!
#                return ["CONJUNCTION"]
#
#        vector = []
#        while cfg.to_node:
#            #TODO: Perform conjunction with the existing value during analysis. 
#            vector.extend(apply(cfg.current_node))
#        return vector
#
#    # Recursively find the fixpoint
#    def rec_apply(previous: list): 
#        res = apply_transfer_functions(cfg, transfer_functions)
#        if res == previous:
#            return res 
#        else:
#            return rec_apply(res)
#    
#    return rec_apply (apply_transfer_functions(cfg, transfer_functions))
