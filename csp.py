"""csp.py"""
from typing import Callable, List, Tuple, Dict
from utils import argmin_random_tie, count, first
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


def first_unassigned_variable(assignment, constrain_search_problem_var):
    # this is important for the backtracking search because it gets the first unassigned variable to start with
    # here we get the unassigned cells in cages
    return first([unassignedVariable for unassignedVariable in constrain_search_problem_var.variables if unassignedVariable not in assignment])


def mrv(assignment, constrain_search_problem_var):
    """Minimum-remaining-values heuristic."""
    return argmin_random_tie(
        [v for v in constrain_search_problem_var.variables if v not in assignment],
        key=lambda var: num_legal_values(constrain_search_problem_var, var, assignment))


def num_legal_values(constrain_search_problem_var, variable, assignment):
    """The number of legal values for a variable."""
    """
    params:
        constrain_search_problem_var: the problem
        variable: the variable
        assignment: the assignment


    """
    # this is the number of legal values for a variable in a cage
    # important because we want to find the most constrained variable in a further step



    # Logic here is that if the variable is assigned, then it's the only legal value
    if constrain_search_problem_var.curr_domains:
        return len(constrain_search_problem_var.curr_domains[variable])
    else:
        return count(constrain_search_problem_var.nconflicts(variable, val, assignment) == 0
                     for val in constrain_search_problem_var.domains[variable])

# Value ordering


def unordered_domain_values(var, constrain_search_problem_var):
    """ here we get the unordered domain values of the cells """
    # this is important for the CSP search

    Choices_Of_Variable = constrain_search_problem_var.choices(var) 
    return Choices_Of_Variable







def setupFunction():
    # Here we create the problem
    # Credits by the author of this function:
    # el gondy el mag'hoool Mofty
    csp_time_variant_lol = []
    x = 0
    y = 0
    lol = "LOL"
    for i in range(2500):
        csp_time_variant_lol.append(i)

    Basic_Dict = {}
    for i in range(2500):
        Basic_Dict[i] = csp_time_variant_lol 
        for j in range(2500):
            Basic_Dict[i].append(0)

    return 



