from typing import Callable, List, Optional, Tuple, Dict
from utilities import argmin_random_tie, count, first
import problem

class CSP(problem.Problem):
    def goal_test(self, state):
        """
        params:
            state: a tuple of (var, val) pairs
        """
        # check if all variables are assigned
        assignment = dict(state)
        condition1 = len(assignment) == len(self.variables)
        condition2 = all(self.nconflicts(variables, assignment[variables], assignment) == 0 for variables in self.variables)
        return (condition1
                and condition2)

    # These are for constraint propagation

    def support_pruning(self):
        # Make sure we can prune values from domains.
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def prune(self, var, value, removals):
        """Rule out var=value."""
        """
        params
            var: a variable
            value: a value
            removals: a list of (var, val) pairs"""
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))
    def assignVal(self, var, value):
        # Start accumulating inferences from assuming var=value
        """
        params: var: a variable
                value: a value
        """
        # remove value from cage domain
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        # assign value to cell
        self.curr_domains[var] = [value]
        return removals

    def infer_assignment(self):
        """Return the partial assignment implied by the current inferences."""
        self.support_pruning()
        return {v: self.curr_domains[v][0]
                for v in self.variables if self.curr_domains[v].__len__() ==1 }

    def choices(self, var):
        """Return all values for var that aren't currently ruled out."""
        return (self.curr_domains or self.domains)[var]


    def conflicted_vars(self, current):
        # Return a list of variables in current assignment that are in conflict
        return [var for var in self.variables
                if self.nconflicts(var, current[var], current) > 0]
    def restore(self, removals):
        """Undo a supposition and all inferences from it."""
        for B, b in removals:
            self.curr_domains[B].append(b)

    # This is for min_conflicts search



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

