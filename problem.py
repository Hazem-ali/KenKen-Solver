"""search.py"""
from typing import List, Optional, Tuple, Dict
from utilities import is_in


class Problem():

    def __init__(
        self,
        initial: List[Tuple[str or int, int]],
        goal: Optional[List[Tuple[str or int, int]]] =None):
        """The constructor specifies the initial state, and possibly a goal
        state, if there is a unique goal."""
        self.initial = initial
        self.goal = goal

    def actions(
        self,
        state: List[Tuple[str or int, int]])->List[List[Tuple[str or int, int]]]:
        """Return the actions that can be executed in the given
        state."""
        raise NotImplementedError

    def result(
        self,
        state:List[Tuple[str or int, int]],
        action:List[Tuple[str or int, int]])->List[Tuple[str or int, int]]:
        """Return the state that results from executing the given
        action in the given state."""
        raise NotImplementedError

    def goal_test(
        self,
        state:List[Tuple[str or int, int]])->bool:
        """Return True if the state is a goal."""
        if isinstance(self.goal, list):
            return is_in(state, self.goal)
        return state == self.goal

    def path_cost(
        self,
        c: int,
        state1: List[Tuple[str or int, int]],
        action: List[Tuple[str or int, int]],
        state2: List[Tuple[str or int, int]])->int:
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1."""
        return c + 1

    def value(
        self,
        state: List[Tuple[str or int, int]])->int:
        raise NotImplementedError
