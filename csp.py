"""csp.py"""
from typing import Callable, List, Tuple, Dict
from utilities import argmin_random_tie, count, first
import problem

class CSP(problem.Problem):
    """This class describes finite-domain Constraint Satisfaction Problems.
    A CSP is specified by the following inputs:
        variables   A list of variables; each is atomic (e.g. int or string).
        domains     A dict of {var:[possible_value, ...]} entries.
        neighbors   A dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
        constraints A function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b

    In the textbook and in most mathematical definitions, the
    constraints are specified as explicit pairs of allowable values,
    but the formulation here is easier to express and more compact for
    most cases. (For example, the n-Queens problem can be represented
    in O(n) space using this notation, instead of O(N^4) for the
    explicit representation.) In terms of describing the CSP as a
    problem, that's all there is.

    However, the class also supports data structures and methods that help you
    solve CSPs by calling a search function on the CSP. Methods and slots are
    as follows, where the argument 'a' represents an assignment, which is a
    dict of {var:val} entries:
        assign(var, val, a)     Assign a[var] = val; do other bookkeeping
        unassign(var, a)        Do del a[var], plus other bookkeeping
        nconflicts(var, val, a) Return the number of other variables that
                                conflict with var=val
        curr_domains[var]       Slot: remaining consistent values for var
                                Used by constraint propagation routines.
    The following methods are used only by graph_search and tree_search:
        actions(state)          Return a list of actions
        result(state, action)   Return a successor of state
        goal_test(state)        Return true if all constraints satisfied
    The following are just for debugging purposes:
        nassigns                Slot: tracks the number of assignments made
        display(a)              Print a human-readable representation
    """

    def __init__(
        self,
        variables: List[str or int],
        domains: Dict[str, int],
        neighbors: Dict[str, List[str]],
        constraints: Callable[[List, int, List, int], bool]):
        """initialize a CSP problem
            Args:
                variables: a list of variables
                domains: a dict of {var:[possible_value, ...]} entries
                neighbors: a dict of {var:[var,...]} that for each variable lists
                    the other variables that participate in constraints.
                    constraints: a function f(A, a, B, b) that returns true if neighbors
                    A, B satisfy the constraint when they have values A=a, B=b
        """
        variables = variables or list(domains.keys())

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.initial = tuple()
        self.curr_domains = None
        self.nassigns = 0

    def assign(
        self,
        var: str or int,
        val: str or int,
        assignment: Dict[str, int]):
        """
            Assign var, if possible, to val in the current assignment.
            Args:
                var: the variable to be assigned
                val: the value to be assigned
                assignment: a dict of {var: val} to be updated
        """
        assignment[var] = val
        self.nassigns += 1

    def unassign(
        self,
        var: str or int,
        assignment: Dict[str, int]):
        """
            Remove var from assignment.
            Args:
                var: the variable to be removed
                assignment: a dict of {var: val}
                Returns:
                    a dict of {var: val}
        """
        if var in assignment:
            del assignment[var]

    def getassignment(
        self,
        assignment: Dict[str, int],
        var: str or int)->int:
        """Return the value of var assigned to in the current assignment"""
        return assignment[var]

    def nconflicts(
        self,
        var: str or int,
        val: str or int,
        assignment: Dict[str, int])->int:
        """
            Return counts conflicts.
        """
        def conflict(
            var2: str or int)->int:
            """
                Return number of conflicts var=val has with var2=assignment[var2]
            """
            return (var2 in assignment and
                    not self.constraints(var, val, var2, self.getassignment(assignment,var2)))
        return count(conflict(v) for v in self.neighbors[var])

    def display(
        self,
        assignment: Dict[str, int]):
        """
            Display the CSP
        Args:
            assignment: a dict of {var: val}
        """
        print('CSP:', self, 'with assignment:', assignment)


    def actions(
        self,
        state: Tuple[str or int, int])->List[Tuple[str or int, int]]:
        """
            Return all actions that can be invoked in the given state.

            Args:
                state: a tuple of (var, val)
            Returns:
                a list of (var, val) tuples
        """
        if state.__len__() == self.variables.__len__():
            return []

        assignment = dict(state)
        var = first(list(filter(lambda v: v not in assignment,
            self.variables)))
        return list(filter(lambda val: self.nconflicts(var, val, assignment) != 0 ,
            self.domains[var]))

    def result(
        self,
        state: Tuple[str or int, int],
        action: Tuple[str or int, int])->Tuple[str or int, int]:
        """
            Update curr_domains to remove values ruled out by previous actions.
                Return an updated state that includes action.
            Args:
                state: a tuple of (var, val)
                action: a tuple of (var, val)
            Returns:
                a tuple of (var, val)
            """
        return state + (action,)
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
