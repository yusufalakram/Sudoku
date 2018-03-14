import numpy as np

# Load sudokus
sudokus = np.load("resources/data/sudokus.npy")
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
    except ValueError:
        return sudoku

    # Store the original value of this blank spot
    originalValue = sudoku[y, x]

    # Store all possible solutions for this blank spot
    possibleSolutions = []
    for value in range(1,10):
        if isPossibleSolution(sudoku, value, x, y):
            possibleSolutions.append(value)

    for value in possibleSolutions:
        print("TRY", value, "FOR [ x:", x, "|", "y:", y, "] FROM:", possibleSolutions)
        sudoku[y, x] = value
        if hasSolutions(sudoku):
            sudoku_solver(sudoku)
        else:
            print("FAIL")
            sudoku[y, x] = originalValue

    """
    # If no solutions are found, raise exception so you can back track
    if not possibleSolutions:
        raise ValueError('No Solution Found')

    # Try all possible solutions, backtracking where necessary
    for value in possibleSolutions:
        try:
            print("TRY", value, "FOR [ x:", x, "|", "y:", y, "] FROM:", possibleSolutions)
            sudoku[y, x] = value
            sudoku_solver(sudoku)
        except ValueError:
            print("failed")
            sudoku[y, x] = originalValue
            continue
    """

def hasSolutions(sudoku):
    # Find a blank spot to fill
    try:
        x, y = findBlankSpace(sudoku)
    # If no blank spots are found, its solved!
    except ValueError:
        return True

    # Store all possible solutions for this blank spot
    possibleSolutions = []
    for value in range(1,10):
        if isPossibleSolution(sudoku, value, x, y):
            possibleSolutions.append(value)

    if not possibleSolutions:
        return False
    else:
        return True

def findBlankSpace(sudoku):
    height, width = np.shape(sudoku)

    for y in range(height):
        for x in range(width):
            if sudoku[y,x] == 0:
                return x, y


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
    concat = []
    for i in range(3):
        for j in range(3):
            if sudoku[gridY+i, gridX+j] == value:
                return False

    # If all tests passed, return True
    return True

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

print("Acutal Puzzle")
print(sudokus[0])
print()
print("Acutal Solution")
print(solutions[0])
print()
print("Calculated Solution:")
print(sudoku_solver(sudokus[0]))


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