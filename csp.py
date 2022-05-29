


# -------------------------------------------------------------------------------------
def AC3(csp_var, queue=None, removals=None):
    # arc consistency 3 algorithm for csp
    """
    params: csp_var: CSP object
            queue: list of arcs to be checked
            removals: list of arcs to be removed    
    """
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp_var.variables for Xk in csp_var.neighbors[Xi]]
    csp_var.support_pruning() 
    # check if queue is empty 
    while len(queue) != 0:
        (Xi, Xj) = queue.pop()
        # remove all values from Xj domain that are not consistent with Xi
        if removeInconsistentValues(csp_var, Xi, Xj, removals):
            if not csp_var.curr_domains[Xi]:
                return False
            for Xk in csp_var.neighbors[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

# -------------------------------------------------------------------------------------

def removeInconsistentValues(csp_var, Xi, Xj, removals):
    # remove inconsistent values from Xj's domain
    """
    params: csp_var: CSP object
            Xi: variable
            Xj: variable
            removals: list of arcs to be removed
    """
    removedVal = False
    for x in csp_var.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp_var.constraints(Xi, x, Xj, y) for y in csp_var.curr_domains[Xj]):
            # prune Xi=x from domain Xj
            csp_var.prune(Xi, x, removals)
            removedVal = True
    return removedVal

# -------------------------------------------------------------------------------------