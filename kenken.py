
import csp

# @ <component>: <usage>

# @ stderr: reporting errors
# @ stdin: receiving input
from sys import stderr

# @ product: creation of the variables' domains
# @ permutations: determine the satisfiability of an operation
from itertools import product, permutations

# @ reduce: determine the result of an operation
from functools import reduce

# @ seed: seed the pseudorandom number generator
# @ random, shuffle, randint, choice: generate a random kenken puzzle
from random import random, shuffle, randint, choice

# @ time: benchmarking
from time import time

# @ writer: output benchmarking data in a csv format
from csv import writer

def operation(operator):
    """
    A utility function used in order to determine the operation corresponding
    to the operator that is given in string format
    """
    if operator == '+':
        return lambda a, b: a + b
    elif operator == '-':
        return lambda a, b: a - b
    elif operator == '*':
        return lambda a, b: a * b
    elif operator == '/':
        return lambda a, b: a / b
    else:
        return None

def adjacent(xy1, xy2):
    """
    Checks wheither two positions represented in 2D coordinates are adjacent
    """
    x1, y1 = xy1
    x2, y2 = xy2

    dx, dy = x1 - x2, y1 - y2

    return (dx == 0 and abs(dy) == 1) or (dy == 0 and abs(dx) == 1)

def generate(size):
    """
    Generate a random kenken puzzle of the given size
      * Initially create a latin square of size 'size' and elements the values [1...size]
      * Shuffle the board by rows and columns in order to get a somewhat random
        board that still satisfies the different row-col constraint of kenken
      * Initialize the 'uncaged' set with all cell coordinates
      * Proceed in creating cellAssignments:
        * Randomly choose a clique size in the range [1..4]
        * Set the first cell in the 'uncaged' set in row major order as
          the root cell of the clique and remove it from the 'uncaged' set
        * Randomly visit at most 'clique-size' 'uncaged' adjacent cells
          in random directions while adding them to the current clique
          and removing them from the 'uncaged' cells
        * The size of the resulting clique is:
          * == 1:
            there is no operation to be performed and the target of the clique
            is equal to the only element of the clique
          * == 2:
            * if the two elements of the clique can be divided without a remainder
              then the operation is set to division and the target is the quotient
            * otherwise, the operation is set to subtraction and the target is the
              difference of the elements
          * >  2:
           randomly choose an operation between addition and multiplication.
            The target of the operation is the result of applying the decided
            operation on all the elements of the clique
        * Continue until the 'uncaged' set is empty i.e. there is no cell belonging
          to no clique
    """

    board = [[((i + j) % size) + 1 for i in range(size)] for j in range(size)]

    # shuffle the board by rows
    for _ in range(size):
        shuffle(board)
    
    # swap
    for c1 in range(size):
        for c2 in range(size):
            if random() > 0.5:
                for r in range(size):
                    board[r][c1], board[r][c2] = board[r][c2], board[r][c1]
    
    # board cells with shuffeld values
    board = {(j + 1, i + 1): board[i][j] for i in range(size) for j in range(size)}

    uncaged = sorted(board.keys(), key=lambda var: var[1])

    # generate cages
    cellAssignments = []
    while uncaged:

        cellAssignments.append([])

        csize = randint(1, 4)

        cell = uncaged[0]

        uncaged.remove(cell)

        cellAssignments[-1].append(cell)

        for _ in range(csize - 1):

            adjs = [other for other in uncaged if adjacent(cell, other)]

            cell = choice(adjs) if adjs else None

            if not cell:
                break

            uncaged.remove(cell)
            
            cellAssignments[-1].append(cell)
            
        csize = len(cellAssignments[-1])
        if csize == 1:
            cell = cellAssignments[-1][0]
            cellAssignments[-1] = ((cell, ), '.', board[cell])
            continue
        elif csize == 2:
            fst, snd = cellAssignments[-1][0], cellAssignments[-1][1]
            if board[fst] / board[snd] > 0 and not board[fst] % board[snd]:
                operator = "/" # choice("+-*/")
            else:
                operator = "-" # choice("+-*")
        else:
            operator = choice("+*")

        target = reduce(operation(operator), [board[cell] for cell in cellAssignments[-1]])

        cellAssignments[-1] = (tuple(cellAssignments[-1]), operator, int(target))

    return size, cellAssignments

def validate(size, cellAssignments):
    """
    Validate the integrity of the input as a kenken board
      * For each of the cellAssignments:
        * Remove duplicate members of the clique at hand
        * Check whether the specified operator is acceptable or not
        * Check if any of the members of the clique are out of bounds
        * Check if any member of the clique is mentioned in any other clique
      * Check if the given cellAssignments cover the whole board or not
    """
    outOfBounds = lambda xy: xy[0] < 1 or xy[0] > size or xy[1] < 1 or xy[1] > size

    mentioned = set()
    for i in range(len(cellAssignments)):
        members, operator, target = cellAssignments[i]

        cellAssignments[i] = (tuple(set(members)), operator, target)

        members, operator, target = cellAssignments[i]

        if operator not in "+-*/.":
            print("Operation", operator, "of clique", cellAssignments[i], "is unacceptable", file=stderr)
            exit(1)

        problematic = list(filter(outOfBounds, members))
        if problematic:
            print("Members", problematic, "of clique", cellAssignments[i], "are out of bounds", file=stderr)
            exit(2)

        problematic = mentioned.intersection(set(members))
        if problematic:
            print("Members", problematic, "of clique", cellAssignments[i], "are cross referenced", file=stderr)
            exit(3)

        mentioned.update(set(members))

    indexes = range(1, size + 1)

    problematic = set([(x, y) for y in indexes for x in indexes]).difference(mentioned)

    if problematic:
        print("Positions", problematic, "were not mentioned in any clique", file=stderr)
        exit(4)

def RowXorCol(xy1, xy2):
    """
    Evaluates to true if the given positions are in the same row / column
    but are in different columns / rows
    """
    return (xy1[0] == xy2[0]) != (xy1[1] == xy2[1])

def conflicting(A, a, B, b):
    """
    Evaluates to true if:
      * there exists mA so that ma is a member of A and
      * there exists mb so that mb is a member of B and
      * RowXorCol(mA, mB) evaluates to true and
      * the value of mA in 'assignment' a is equal to
        the value of mb in 'assignment' b
    """
    for i in range(len(A)):
        for j in range(len(B)):
            mA = A[i]
            mB = B[j]

            ma = a[i]
            mb = b[j]
            if RowXorCol(mA, mB) and ma == mb:
                return True

    return False

def satisfies(values, operation, target):
    """
    Evaluates to true if the result of applying the operation
    on a permutation of the given values is equal to the specified target
    """
    for p in permutations(values):
        if reduce(operation, p) == target:
            return True

    return False

def gdomains(size, cellAssignments):
    """
    @ https://docs.python.org/2/library/itertools.html
    @ product('ABCD', repeat=2) = [AA AB AC AD BA BB BC BD CA CB CC CD DA DB DC DD]

    For every clique in cellAssignments:
        * Initialize the domain of each variable to contain every product
        of the set [1...board-size] that are of length 'clique-size'.
        For example:

            board-size = 3 and clique-size = 2

            products = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3)]

        * Discard any value (assignment of the members of the clique) that:
        * is resulting in the members of the clique 'conflicting' with each other
        * does not 'satisfy' the given operation
    """
    domains = {}
    for clique in cellAssignments:
        members, operator, target = clique

        domains[members] = list(product(range(1, size + 1), repeat=len(members)))

        qualifies = lambda values: not conflicting(members, values, members, values) and satisfies(values, operation(operator), target)

        domains[members] = list(filter(qualifies, domains[members]))

    return domains

def gneighbors(cellAssignments):
    """
    Determine the neighbors of each variable for the given puzzle
        For every clique in cellAssignments
        * Initialize its neighborhood as empty
        * For every clique in cellAssignments other than the clique at hand,
            if they are probable to 'conflict' they are considered neighbors
    """
    neighbors = {}
    for members, _, _ in cellAssignments:
        neighbors[members] = []

    for A, _, _ in cellAssignments:
        for B, _, _ in cellAssignments:
            if A != B and B not in neighbors[A]:
                if conflicting(A, [-1] * len(A), B, [-1] * len(B)):
                    neighbors[A].append(B)
                    neighbors[B].append(A)

    return neighbors

class Kenken(csp.CSP):

    def __init__(self, size, cellAssignments):
        """
        In my implementation, I consider the cellAssignments themselves as variables.
        A clique is of the format (((X1, Y1), ..., (XN, YN)), <operation>, <target>)
        where
            * (X1, Y1), ..., (XN, YN) are the members of the clique
            * <operation> is either addition, subtraction, division or multiplication
            * <target> is the value that the <operation> should produce
              when applied on the members of the clique
        """
        validate(size, cellAssignments)
        
        variables = [members for members, _, _ in cellAssignments]
        
        domains = gdomains(size, cellAssignments)

        neighbors = gneighbors(cellAssignments)

        csp.CSP.__init__(self, variables, domains, neighbors, self.constraint)

        self.size = size

        # Used in benchmarking
        self.checks = 0

        # Used in displaying
        self.padding = 0

        self.meta = {}
        for members, operator, target in cellAssignments:
            self.meta[members] = (operator, target)
            self.padding = max(self.padding, len(str(target)))        


    def constraint(self, A, a, B, b):
        """
        Any two variables satisfy the constraint if they are the same
        or they are not 'conflicting' i.e. every member of variable A
        which shares the same row or column with a member of variable B
        must not have the same value assigned to it
        """
        self.checks += 1

        return A == B or not conflicting(A, a, B, b)

def benchmark(kenken, algorithm):
        """
        Used in order to benchmark the given algorithm in terms of
          * The number of nodes it visits
          * The number of constraint checks it performs
          * The number of assignments it performs
          * The completion time
        """
        kenken.checks = kenken.nassigns = 0

        dt = time()

        assignment = algorithm(kenken)

        dt = time() - dt

        return assignment, (kenken.checks, kenken.nassigns, dt)

def gather(iterations, out):
    """
    Benchmark each one of the following algorithms for various kenken puzzles

      * For every one of the following algorithms
       * For every possible size of a kenken board
         * Create 'iterations' random kenken puzzles of the current size
           and evaluate the algorithm on each one of them in order to get
           statistically sound data. Then calculate the average evaluation
           of the algorithm for the current size.

      * Save the results into a csv file
    """
    bt         = lambda ken: csp.backtracking_search(ken)
    fc         = lambda ken: csp.backtracking_search(ken, inference=csp.forward_checking)
    mac        = lambda ken: csp.backtracking_search(ken, inference=csp.mac)


    algorithms = {
        "BT": bt,
        "FC": fc,
        "MAC": mac,
    }

    with open(out, "w+") as file:

        out = writer(file)

        out.writerow(["Algorithm", "Size", "Result", "Constraint checks", "Assignments", "Completion time"])

        for name, algorithm in algorithms.items():
            for size in range(3, 10):
                checks, assignments, dt = (0, 0, 0)
                for iteration in range(1, iterations + 1):
                    size, cellAssignments = generate(size)

                    assignment, data = benchmark(Kenken(size, cellAssignments), algorithm)

                    print("algorithm =",  name, "size =", size, "iteration =", iteration, "result =", "Success" if assignment else "Failure", file=stderr)

                    checks      += data[0] / iterations
                    assignments += data[1] / iterations
                    dt          += data[2] / iterations
                    
                out.writerow([name, size, checks, assignments, dt])

def solve(
    size:int,
    cellAssignments,
    algorithm:str):
    ken = Kenken(size, cellAssignments)
    if algorithm == "Backtracking":
        return csp.backtracking_search(ken)
    elif algorithm == "Forward Checking":
        return csp.backtracking_search(ken, inference=csp.forward_checking)
    elif algorithm == "Arc Consistency":
        return csp.backtracking_search(ken, inference=csp.mac)
    return None

    # benchmark all algorithms
    # gather(100, "benchmark.csv")

# kenken.py ends here