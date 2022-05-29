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