import numpy as np
import timeit


# Load sudokus
sudokus = np.load("resources/data/sudokus.npy")
oneksudokus = np.load("resources/data/sudoku-sample-1000.npy")
#print("Shape of sudokus array:", sudokus.shape, "; Type of array values:", sudokus.dtype)

# Load solutions
solutions = np.load("resources/data/solutions.npy")
#print("Shape of solutions array:", solutions.shape, "; Type of array values:", solutions.dtype, "\n")

"""
# Print the first sudoku...
print("Sudoku #1:")
print(sudokus[0], "\n")

# ...and its solution
print("Solution of Sudoku #1:")
print(solutions[0])
"""

def sudoku_solver(sudoku):
    dict = generate_dictionary(sudoku)

    # If a single position is empty, return np.full((9,9),-1)
    for key in dict:
        if not dict[key]:
            return np.full((9, 9), -1)

    # Try out all values using dictionary and backtracking
    return sudoku_solver_w(sudoku)


def sudoku_solver_w(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.
    Input
        sudoku : 9x9 numpy array of integers
            Empty cells are designated by 0.
    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """
    # Find a blank spot to fill
    try:
        x, y = findBlankSpace(sudoku)
    # If no blank spots are found, its solved!
    except noBlanksFound:
        return sudoku

    # Store all possible solutions for this blank spot
    possible_solutions = []
    for value in range(1,10):
        if isPossibleSolution(sudoku, value, x, y):
            possible_solutions.append(value)


    # Keep copy of current board on recursive stack
    solved_sudoku = np.copy(sudoku)

    # Try all possible solutions, backtracking where necessary
    for value in possible_solutions:
        try:
            #print("TRY", value, "FOR [ x:", x, "|", "y:", y, "] FROM:", possible_solutions)
            solved_sudoku[y, x] = value
            return sudoku_solver_w(solved_sudoku)
        except noSolutionFound:
            #print("failed")
            continue

    raise noSolutionFound()


def findBlankSpace(sudoku):
    height, width = np.shape(sudoku)
    for y in range(height):
        for x in range(width):
            if sudoku[y, x] == 0:
                return x, y
    raise noBlanksFound('No blank space found')


class noBlanksFound(Exception):
    pass


class noSolutionFound(Exception):
    pass


def generate_dictionary(sudoku):
    height, width = np.shape(sudoku)

    dict = {}

    for y in range(height):
        for x in range(width):
            if sudoku[y,x] != 0:
                continue
            possibleValues = []
            for value in range(1,10):
                if isPossibleSolution(sudoku, value, x, y):
                    possibleValues.append(value)
            dict[(x, y)] = possibleValues

    return dict


def isPossibleSolution(sudoku, value, xCoord, yCoord):
    # Initialize height & width of puzzle
    height, width = np.shape(sudoku)

    # Row y must not contain value
    for x in range(width):
        if sudoku[yCoord,x] == value:
            return False

    # Column x must not contain value
    for y in range(height):
        if sudoku[y,xCoord] == value:
            return False

    # This 3x3 grid must not contain value
    gridY = yCoord - (yCoord % 3)
    gridX = xCoord - (xCoord % 3)

    # Check if this number is unique within this 3x3 grid
    for i in range(3):
        for j in range(3):
            if sudoku[gridY+i, gridX+j] == value:
                return False

    # If all tests passed, return True
    return True


# Impossible test
"""
sudoku1 = sudokus[0];
sudoku1[1,0] = 7
print(sudoku1)
print(sudoku_solver(sudoku1))
"""

# Fuck me up
"""
fuckmeup = np.array([
         [4,0,0,0,0,0,0,0,9],
         [8,0,0,6,0,0,0,0,0],
         [0,0,0,0,0,5,1,0,0],
         [0,0,0,0,0,0,0,6,8],
         [0,2,0,0,0,3,0,0,0],
         [0,0,0,0,0,0,0,0,4],
         [0,0,5,0,0,0,2,0,0],
         [0,0,0,4,3,0,0,0,0],
         [0,7,0,0,8,0,0,0,0],
         ])
print(sudoku_solver(fuckmeup))
"""

# Actual test

a = timeit.default_timer()
for i in range(100):
    print("Puzzle",i,"result:",np.array_equal(sudoku_solver(sudokus[i]), solutions[i]))
b = timeit.default_timer()
print("time taken:", (b-a))


# One thousand test
"""
a = timeit.default_timer()
for i in range(1000):
    print("Puzzle",i,"result:")
    print(sudoku_solver(oneksudokus[i]))
b = timeit.default_timer()
print("time taken:", (b-a))
"""


# Test for isPossibleSolution
"""
print("Acutal Puzzle")
print(sudokus[0])
print()
sudoku = sudokus[0]
possibleSolutions = []
for value in range(1, 10):
    if isPossibleSolution(sudoku, value, 4, 3):
        possibleSolutions.append(value)
print(possibleSolutions)
"""

# Test for puzzle
"""
print("Acutal Puzzle")
print(sudokus[0])
print()
print("Acutal Solution")
print(solutions[0])
print()
print("Calculated Solution:")
print(sudoku_solver(sudokus[0]))
"""

# Old tests
"""
print()
print("Calculated solution of Sudoku #2:")
print(sudoku_solver(sudokus[1]))


#sudoku1 = sudokus[0];
#sudoku1[1,0] = 7
#sudoku1[8,7] = 5
#print(sudoku1)
#print()
#print("solvable?")
#print(solvable(sudoku1))
#print(sudoku_solver(sudoku1))


def solvable(sudoku):
    # Initialize height & width of puzzle
    height, width = np.shape(sudoku)

    # All numbers in each row must be unique
    for y in range(height):
        row_uniques, row_counts = np.unique(sudoku[y,:], return_counts=True)
        if all(i <= 1 for i in row_counts[1:]):
            continue
        else:
            return False

    # All numbers in each column must be unique
    for x in range(width):
        column_uniques, column_counts = np.unique(sudoku[x,:], return_counts=True)
        if all(i <= 1 for i in column_counts[1:]):
            continue
        else:
            return False

    # All numbers in each 3x3 box must be unique
    # Check all nine 3x3 regions
    for y in [0,3,6]:
        for x in [0,3,6]:

            # Concatenate all elements of this region
            concat = []
            for i in range(3):
                for j in range(3):
                    concat.append(sudoku[y+i, x+j])

            # Check if unique
            elem_uniques, elem_counts = np.unique(concat, return_counts=True)
            if all(i<=1 for i in elem_counts[1:]):
                continue
            else:
                return False

    # If all tests passed, return true
    return True
"""